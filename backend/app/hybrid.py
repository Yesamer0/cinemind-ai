import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from backend.app.content_based import recommend_movies
from backend.app.data_loader import load_catalog
from backend.app.semantic_search import faiss_similar_movies, load_semantic_index


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




def rank_recommendations(liked_movies, rated_movie_ids, limit=10):
    movies = load_catalog()
    movie_embeddings, _ = load_semantic_index()
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

    return recommendations[:limit]
