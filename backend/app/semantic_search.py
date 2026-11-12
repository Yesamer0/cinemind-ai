import os
import pickle
from functools import lru_cache
from pathlib import Path
from tempfile import NamedTemporaryFile
from threading import Lock

import faiss
import numpy as np

from backend.app.config import BASE_DIR
from backend.app.data_loader import load_catalog

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384
_index_lock = Lock()


@lru_cache(maxsize=1)
def load_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(MODEL_NAME)


def build_embeddings(path, overviews):
    vectors = load_model().encode(overviews, show_progress_bar=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=path.parent, delete=False) as file:
        temporary_path = Path(file.name)
    try:
        with temporary_path.open("wb") as file:
            pickle.dump(vectors, file)
        temporary_path.replace(path)
    finally:
        temporary_path.unlink(missing_ok=True)
    return vectors


def load_semantic_index():
    with _index_lock:
        return _load_semantic_index()


@lru_cache(maxsize=1)
def _load_semantic_index():
    catalog = load_catalog()
    path = Path(os.getenv("EMBEDDINGS_PATH", BASE_DIR / "movie_embeddings.pkl"))
    if path.exists():
        with path.open("rb") as file:
            vectors = pickle.load(file)
    else:
        vectors = build_embeddings(path, catalog["overview"].tolist())

    embeddings = np.array(vectors, dtype="float32", order="C", copy=True)
    if embeddings.shape != (len(catalog), EMBEDDING_DIMENSION):
        raise ValueError(f"{path} does not match the movie catalog. Regenerate the embeddings.")

    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(EMBEDDING_DIMENSION)
    index.add(embeddings)
    return embeddings, index


def encode_query(query):
    embedding = np.asarray(load_model().encode([query]), dtype="float32")
    faiss.normalize_L2(embedding)
    return embedding


def semantic_search(query, top_n=5):
    movies = load_catalog()
    _, faiss_index = load_semantic_index()
    scores, indices = faiss_index.search(encode_query(query), top_n)

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
    movies = load_catalog()
    movie_embeddings, faiss_index = load_semantic_index()

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
