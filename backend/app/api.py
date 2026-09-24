from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv
from jose import jwt

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.app.database import Base, engine, get_db
from backend.app.models import User, Favorite, Rating
from backend.app.semantic_search import (
    semantic_search,
    faiss_similar_movies,
    movies,
    movie_embeddings
)
from backend.app.content_based import (
    recommend_movies,
    recommend_by_keyword
)

from backend.app.llm_service import understand_movie_request

load_dotenv("backend/.env")

# Create the FastAPI application instance
app = FastAPI()
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not configured."
    )
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
ALGORITHM = "HS256"


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to CineMind API!"
    }

# Search endpoint
@app.get("/search")
def search_movies(
    query: str = Query(..., min_length=2, description="Movie search query"),
    limit: int = Query(5, ge=1, le=20)
):
    results = semantic_search(query, top_n=limit)

    return {
        "query": query,
        "total_results": len(results),
        "results": results
    }

@app.get("/keyword-recommendations")
def keyword_recommendations(
    query: str = Query(
        ...,
        min_length=2,
        description="Keyword for movie recommendation"
    )
):
    results = recommend_by_keyword(query)

    recommendations = []

    for index, movie in results.iterrows():
        recommendations.append({
            "id": int(index),
            "title": movie["title"],
            "overview": movie["overview"]
        })

    return {
        "query": query,
        "total_results": len(recommendations),
        "results": recommendations
    }

@app.get("/movies")
def get_movies(
    limit: int = 20,
    offset: int = 0,
    sort: str = "id"
):

    if sort == "title":
        sorted_movies = movies.sort_values("title")
    else:
        sorted_movies = movies

    selected_movies = sorted_movies.iloc[
        offset:offset + limit
    ]

    results = []

    for movie_index, movie in selected_movies.iterrows():

        results.append({
            "id": int(movie_index),
            "title": movie["title"],
            "overview": movie["overview"],
            "poster_path": movie["poster_path"],
            "rating": movie["vote_average"]
        })

    return results
# Return the first 10 movies when the application starts.
@app.get("/popular")
def popular_movies(
    limit: int = Query(10, ge=1, le=50)
):

    popular = movies.copy()

    # Convert numeric columns safely
    popular["popularity"] = pd.to_numeric(
        popular["popularity"],
        errors="coerce"
    )

    popular["vote_count"] = pd.to_numeric(
        popular["vote_count"],
        errors="coerce"
    )

    # Remove rows with invalid popularity values
    popular = popular.dropna(
        subset=["popularity"]
    )

    # Sort movies by popularity
    popular = popular.sort_values(
        by="popularity",
        ascending=False
    ).head(limit)

    results = []

    for movie_index, movie in popular.iterrows():

        results.append({
            "id": int(movie_index),
            "title": movie["title"],
            "overview": movie["overview"],
            "genres": movie["genres"],
            "rating": movie["vote_average"],
            "vote_count": (
                0
                if pd.isna(movie["vote_count"])
                else int(movie["vote_count"])
            ),
            "popularity": float(movie["popularity"]),
            "release_date": movie["release_date"],
            "poster_path": movie["poster_path"]
        })

    return results

@app.get("/movie/{movie_id}")
def get_movie(movie_id: int):

    if movie_id < 0 or movie_id >= len(movies):
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    movie = movies.iloc[movie_id]

    return {
    "id": movie_id,
    "title": movie["title"],
    "overview": movie["overview"],
    "genres": movie["genres"],
    "rating": movie["vote_average"],
    "release_date": movie["release_date"],
    "poster_path": movie["poster_path"]
}


@app.post("/register")
def register_user(
    username: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        (User.username == username) |
        (User.email == email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    hashed_password = pwd_context.hash(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "username": new_user.username
    }


@app.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    if not pwd_context.verify(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    token = jwt.encode(
        {
            "sub": str(user.id),
            "username": user.username
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


@app.post("/favorites/{movie_id}")
def add_favorite(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing_favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.movie_id == movie_id
    ).first()

    if existing_favorite:
        raise HTTPException(
            status_code=400,
            detail="Movie already in favorites"
        )

    favorite = Favorite(
        user_id=current_user.id,
        movie_id=movie_id
    )

    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return {
        "message": "Movie added to favorites",
        "movie_id": movie_id
    }  



@app.get("/favorites")
def get_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    favorites = db.query(Favorite).filter(
        Favorite.user_id == current_user.id
    ).all()

    return [
        {
            "movie_id": favorite.movie_id
        }
        for favorite in favorites
    ]


@app.delete("/favorites/{movie_id}")
def remove_favorite(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.movie_id == movie_id
    ).first()

    if favorite is None:
        raise HTTPException(
            status_code=404,
            detail="Movie is not in favorites"
        )

    db.delete(favorite)
    db.commit()

    return {
        "message": "Movie removed from favorites",
        "movie_id": movie_id
    }


@app.post("/ratings/{movie_id}")
def rate_movie(
    movie_id: int,
    rating: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if rating < 1 or rating > 5:
        raise HTTPException(
            status_code=400,
            detail="Rating must be between 1 and 5"
        )

    existing_rating = db.query(Rating).filter(
        Rating.user_id == current_user.id,
        Rating.movie_id == movie_id
    ).first()

    if existing_rating:

        existing_rating.rating = rating

    else:

        new_rating = Rating(
            user_id=current_user.id,
            movie_id=movie_id,
            rating=rating
        )

        db.add(new_rating)

    db.commit()

    return {
        "message": "Movie rated successfully",
        "movie_id": movie_id,
        "rating": rating
    }


@app.get("/ratings/{movie_id}")
def get_movie_rating(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    rating = db.query(Rating).filter(
        Rating.user_id == current_user.id,
        Rating.movie_id == movie_id
    ).first()

    if rating is None:

        return {
            "movie_id": movie_id,
            "rating": None
        }

    return {
        "movie_id": movie_id,
        "rating": rating.rating
    }


def add_hybrid_candidate(
    recommendation_map,
    movie,
    movie_index,
    content_similarity,
    semantic_similarity
):

    # --------------------------------
    # TMDB RATING
    # --------------------------------

    tmdb_rating = pd.to_numeric(
        movie["vote_average"],
        errors="coerce"
    )

    if pd.isna(tmdb_rating):
        tmdb_rating = 0.0

    normalized_rating = (
        float(tmdb_rating) / 10.0
    )

    # --------------------------------
    # POPULARITY
    # --------------------------------

    popularity = pd.to_numeric(
        movie["popularity"],
        errors="coerce"
    )

    if pd.isna(popularity):
        popularity = 0.0

    normalized_popularity = min(
        max(
            float(popularity) / 100.0,
            0.0
        ),
        1.0
    )

    # --------------------------------
    # FINAL HYBRID SCORE
    # --------------------------------

    hybrid_score = (
        content_similarity * 0.40
        + semantic_similarity * 0.30
        + normalized_rating * 0.20
        + normalized_popularity * 0.10
    )

    movie_data = {
        "id": int(movie_index),
        "title": movie["title"],
        "overview": movie["overview"],
        "genres": movie["genres"],
        "rating": float(tmdb_rating),
        "release_date": movie["release_date"],
        "poster_path": movie["poster_path"],

        "content_similarity": round(
            float(content_similarity),
            4
        ),

        "semantic_similarity": round(
            float(semantic_similarity),
            4
        ),

        "hybrid_score": round(
            float(hybrid_score),
            4
        )
    }

    # Same movie can come from both TF-IDF and FAISS.
    # Keep the version with the best hybrid score.
    if (
        movie_index not in recommendation_map
        or hybrid_score >
        recommendation_map[
            movie_index
        ]["hybrid_score"]
    ):
        recommendation_map[
            movie_index
        ] = movie_data


@app.get("/recommendations")
def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # --------------------------------
    # 1. GET USER RATINGS
    # --------------------------------

    ratings = db.query(Rating).filter(
        Rating.user_id == current_user.id
    ).all()

    # Movies rated 4 or 5 are considered liked
    liked_movies = [
        rating.movie_id
        for rating in ratings
        if rating.rating >= 4
    ]

    if not liked_movies:
        return {
            "message": "Rate some movies first to get recommendations.",
            "results": []
        }

    # Movies already rated by the user
    rated_movie_ids = {
        rating.movie_id
        for rating in ratings
    }

    recommendation_map = {}

    # --------------------------------
    # 2. PROCESS EACH LIKED MOVIE
    # --------------------------------

    for liked_movie_id in liked_movies:

        if (
            liked_movie_id < 0
            or liked_movie_id >= len(movies)
            or liked_movie_id >= len(movie_embeddings)
        ):
            continue

        liked_movie = movies.iloc[
            liked_movie_id
        ]

        liked_movie_title = liked_movie[
            "title"
        ]

        liked_embedding = movie_embeddings[
            liked_movie_id
        ]

                # ========================================
        # A) TF-IDF CANDIDATES
        # ========================================

        # Calculate TF-IDF similarities only ONCE
        content_candidates_extended = recommend_movies(
            liked_movie_title,
            top_n=20
        )

        # If no recommendations are found, use empty list
        if not content_candidates_extended:
            content_candidates_extended = []

        # Top 5 will be used as direct TF-IDF candidates
        content_candidates = content_candidates_extended[:5]

        # Store the top 20 scores for FAISS candidates
        content_score_map = {
            candidate["title"]: float(
                candidate["similarity"]
            )
            for candidate in content_candidates_extended
        }

        # Process TF-IDF candidates
        for candidate in content_candidates:

            candidate_title = candidate["title"]

            content_similarity = float(
                candidate["similarity"]
            )

            movie_match = movies[
                movies["title"] == candidate_title
            ]

            if movie_match.empty:
                continue

            movie_index = int(
                movie_match.index[0]
            )

            if movie_index in rated_movie_ids:
                continue

            if movie_index >= len(movie_embeddings):
                continue

            movie = movie_match.iloc[0]

            candidate_embedding = movie_embeddings[
                movie_index
            ]

            semantic_similarity = float(
                cosine_similarity(
                    [liked_embedding],
                    [candidate_embedding]
                )[0][0]
            )

            add_hybrid_candidate(
                recommendation_map,
                movie,
                movie_index,
                content_similarity,
                semantic_similarity
            )

        # ========================================
        # B) FAISS SEMANTIC CANDIDATES
        # ========================================

        semantic_candidates = faiss_similar_movies(
            liked_movie_id,
            top_n=5
        )

        for candidate in semantic_candidates:

            movie_index = candidate["id"]

            if movie_index in rated_movie_ids:
                continue

            if (
                movie_index < 0
                or movie_index >= len(movies)
            ):
                continue

            movie = movies.iloc[
                movie_index
            ]

            semantic_similarity = float(
                candidate["semantic_similarity"]
            )

            # Reuse TF-IDF scores calculated above
            content_similarity = content_score_map.get(
                movie["title"],
                0.0
            )

            add_hybrid_candidate(
                recommendation_map,
                movie,
                movie_index,
                content_similarity,
                semantic_similarity
            )

    # --------------------------------
    # 3. FINAL RANKING
    # --------------------------------

    recommendations = list(
        recommendation_map.values()
    )

    recommendations.sort(
        key=lambda movie: movie["hybrid_score"],
        reverse=True
    )

    return {
        "results": recommendations[:10]
    }



@app.get("/ai-recommend")
def ai_recommend(
    query: str = Query(
        ...,
        min_length=3,
        description="Natural language movie request"
    )
):

    # 1. Understand the user's natural-language request
    llm_result = understand_movie_request(
        query
    )

    semantic_query = llm_result[
        "semantic_query"
    ]

    # 2. Search the movie vector database
    results = semantic_search(
        semantic_query,
        top_n=10
    )

    # 3. Return both the interpreted query
    # and the movies found by FAISS
    return {
        "original_query": query,
        "semantic_query": semantic_query,
        "llm_used": llm_result.get(
            "llm_used",
            False
        ),
        "provider": llm_result.get(
            "provider",
            "fallback"
        ),
        "results": results
    }