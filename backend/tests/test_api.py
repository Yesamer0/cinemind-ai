from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app import main
from backend.app.api import app
from backend.app.database import get_db
from backend.app.routers import recommendations


@pytest.fixture
def client(tmp_path, monkeypatch):
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")

    def test_db():
        with Session(engine) as session:
            yield session

    monkeypatch.setenv("SECRET_KEY", "local-test-secret")
    monkeypatch.setattr(main, "engine", engine)
    app.dependency_overrides[get_db] = test_db
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        engine.dispose()


@pytest.fixture
def registered_user(client):
    user = {"username": "tester", "email": "test@example.com", "password": "test-password"}
    assert client.post("/register", params=user).status_code == 200
    return {"username": user["username"], "password": user["password"]}


@pytest.fixture
def headers(client, registered_user):
    response = client.post("/login", data=registered_user)
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_home(client):
    assert client.get("/").json() == {"message": "Welcome to CineMind API!"}


def test_login_rejects_wrong_password(client, registered_user):
    response = client.post("/login", data={**registered_user, "password": "wrong-password"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_login_issues_token_with_one_hour_expiry(client, registered_user):
    started_at = int(datetime.now(timezone.utc).timestamp())
    response = client.post("/login", data=registered_user)
    finished_at = int(datetime.now(timezone.utc).timestamp())

    assert response.status_code == 200
    claims = jwt.get_unverified_claims(response.json()["access_token"])
    assert started_at + 3600 <= claims["exp"] <= finished_at + 3600


@pytest.mark.parametrize("expiration", [{"exp": 1}, {}], ids=["expired", "missing-exp"])
def test_favorites_reject_invalid_expiration(client, headers, expiration):
    token = headers["Authorization"].removeprefix("Bearer ")
    claims = jwt.get_unverified_claims(token)
    del claims["exp"]
    token = jwt.encode({**claims, **expiration}, "local-test-secret", algorithm="HS256")

    response = client.get("/favorites", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def test_favorites_require_authentication(client):
    assert client.get("/favorites").status_code == 401


def test_favorites_lifecycle(client, headers):
    assert client.post("/favorites/12", headers=headers).status_code == 200
    assert client.post("/favorites/12", headers=headers).status_code == 400
    assert client.get("/favorites", headers=headers).json() == [{"movie_id": 12}]
    assert client.delete("/favorites/12", headers=headers).status_code == 200
    assert client.get("/favorites", headers=headers).json() == []


def test_rating_validation_and_update(client, headers):
    assert client.post("/ratings/12?rating=6", headers=headers).status_code == 400
    for rating in (3, 5):
        assert client.post(f"/ratings/12?rating={rating}", headers=headers).status_code == 200
    assert client.get("/ratings/12", headers=headers).json() == {"movie_id": 12, "rating": 5}


def test_recommendations_without_liked_movies(client, headers):
    assert client.get("/recommendations", headers=headers).json()["results"] == []


def test_recommendations_use_likes_and_exclude_all_rated_movies(client, headers, monkeypatch):
    def rank(liked, rated):
        assert liked == [12]
        assert rated == {12, 23}
        return [{"id": 34}]

    monkeypatch.setattr(recommendations, "rank_recommendations", rank)
    client.post("/ratings/12?rating=5", headers=headers)
    client.post("/ratings/23?rating=2", headers=headers)
    assert client.get("/recommendations", headers=headers).json() == {"results": [{"id": 34}]}


def test_search_validates_limit(client):
    assert client.get("/search", params={"query": "space", "limit": 21}).status_code == 422
