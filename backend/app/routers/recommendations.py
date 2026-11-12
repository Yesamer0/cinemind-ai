from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.content_based import recommend_by_keyword
from backend.app.database import get_db
from backend.app.hybrid import rank_recommendations
from backend.app.llm_service import understand_movie_request
from backend.app.models import Rating, User
from backend.app.routers.auth import get_current_user
from backend.app.semantic_search import semantic_search

router = APIRouter()


@router.get("/search")
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

@router.get("/keyword-recommendations")
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

@router.get("/recommendations")
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

    return {"results": rank_recommendations(liked_movies, rated_movie_ids)}


@router.get("/ai-recommend")
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
