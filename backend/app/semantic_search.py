import pickle
import os
import pandas as pd

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

def semantic_search(query, top_n=5):

    # Convert user query into an embedding
    query_embedding = model.encode(query)

    # Calculate cosine similarity
    similarities = cosine_similarity(
        [query_embedding],
        movie_embeddings
    )[0]

    # Sort movies by similarity score
    sorted_indices = similarities.argsort()[::-1]

    # Get top N movie indices
    top_indices = sorted_indices[:top_n]

    results = []

    for idx in top_indices:
        results.append({
    "id": int(idx),
    "title": str(movies.iloc[idx]["title"]),
    "overview": str(movies.iloc[idx]["overview"]),
    "score": round(float(similarities[idx]), 3),
    "poster_path": (
        None
        if pd.isna(movies.iloc[idx]["poster_path"])
        else str(movies.iloc[idx]["poster_path"])
    )
})

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

