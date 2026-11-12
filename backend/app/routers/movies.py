import pandas as pd
from fastapi import APIRouter, HTTPException, Query

from backend.app.data_loader import load_catalog

router = APIRouter()


@router.get("/movies")
def get_movies(
    limit: int = 20,
    offset: int = 0,
    sort: str = "id"
):

    movies = load_catalog()
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
@router.get("/popular")
def popular_movies(
    limit: int = Query(10, ge=1, le=50)
):

    popular = load_catalog().copy()

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

@router.get("/movie/{movie_id}")
def get_movie(movie_id: int):
    movies = load_catalog()

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
