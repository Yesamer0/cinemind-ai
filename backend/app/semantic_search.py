import pickle
import os
import pandas as pd

import numpy as np
import faiss

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from backend.app.data_loader import load_tmdb_movies


print("Loading AI model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully!")


movies = load_tmdb_movies()
print(movies.columns.tolist())
print("\nNumber of Movies")
print(len(movies))


movies = movies[
    [
        "title",
        "overview",
        "genres",
        "vote_average",
        "vote_count",
        "popularity",
        "release_date",
        "poster_path"
    ]
]
movies = movies.dropna(
    subset=["overview"]
).reset_index(drop=True)

print("\nFirst Movies")
print(movies.head())

embedding_file = "movie_embeddings.pkl"

if os.path.exists(embedding_file):

    print("Loading saved embeddings...")

    with open(embedding_file, "rb") as f:
        movie_embeddings = pickle.load(f)

else:

    print("Creating embeddings...")

    movie_embeddings = model.encode(
        movies["overview"].tolist(),
        show_progress_bar=True
    )

    with open(embedding_file, "wb") as f:
        pickle.dump(movie_embeddings, f)

    print("Embeddings saved successfully!")

print(movie_embeddings.shape)

# --------------------------------
# FAISS VECTOR INDEX
# --------------------------------

# Convert embeddings to float32
faiss_embeddings = np.asarray(
    movie_embeddings,
    dtype="float32"
)

# Normalize vectors so inner product
# behaves like cosine similarity
faiss.normalize_L2(faiss_embeddings)

# Embedding dimension (384 for MiniLM)
embedding_dimension = faiss_embeddings.shape[1]

# Create FAISS index
faiss_index = faiss.IndexFlatIP(
    embedding_dimension
)

# Add all movie embeddings to the index
faiss_index.add(
    faiss_embeddings
)

print(
    "FAISS index created:",
    faiss_index.ntotal,
    "movies"
)

def semantic_search(query, top_n=5):

    # --------------------------------
    # 1. Convert user query to vector
    # --------------------------------

    query_embedding = model.encode(
        [query]
    )

    # FAISS expects float32
    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    # Same normalization used for movie embeddings
    faiss.normalize_L2(
        query_embedding
    )

    # --------------------------------
    # 2. Search FAISS index
    # --------------------------------

    scores, indices = faiss_index.search(
        query_embedding,
        top_n
    )

    # --------------------------------
    # 3. Prepare API results
    # --------------------------------

    results = []

    for score, movie_index in zip(
        scores[0],
        indices[0]
    ):

        # FAISS can theoretically return -1
        # when no valid result exists
        if movie_index == -1:
            continue

        movie = movies.iloc[
            int(movie_index)
        ]

        results.append({
            "id": int(movie_index),
            "title": movie["title"],
            "overview": movie["overview"],
            "score": float(score),
            "poster_path": movie["poster_path"]
        })

    return results


def faiss_similar_movies(movie_id, top_n=5):

    # Check whether movie ID is valid
    if movie_id < 0 or movie_id >= len(movie_embeddings):
        return []

    # Get the selected movie's embedding
    query_embedding = np.asarray(
        [movie_embeddings[movie_id]],
        dtype="float32"
    )

    # Normalize for cosine-style similarity
    faiss.normalize_L2(
        query_embedding
    )

    # +1 because the movie itself will usually
    # be the closest result
    scores, indices = faiss_index.search(
        query_embedding,
        top_n + 1
    )

    results = []

    for score, movie_index in zip(
        scores[0],
        indices[0]
    ):

        movie_index = int(movie_index)

        # Invalid FAISS result
        if movie_index == -1:
            continue

        # Do not recommend the same movie
        if movie_index == movie_id:
            continue

        movie = movies.iloc[movie_index]

        results.append({
            "id": movie_index,
            "title": movie["title"],
            "overview": movie["overview"],
            "poster_path": movie["poster_path"],
            "semantic_similarity": float(score)
        })

        if len(results) >= top_n:
            break

    return results

# Main function: starts the program and handles user interaction.
# It runs only when this file is executed directly.
def main():

    query = input(
        "\nWhat kind of movie are you looking for?\n> "
    )

    results = semantic_search(query)

    print("\nSemantic Search Results\n")

    for movie in results:

        print(
            movie["title"],
            "- Score:",
            movie["score"]
        )


if __name__ == "__main__":
    main()

