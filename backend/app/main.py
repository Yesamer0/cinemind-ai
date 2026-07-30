import pandas as pd
from recommender import (
    top_rated_movies,
    recommend_by_genre,
    best_movies_by_genre,
    display_movies
)


from data_loader import (
    load_movies,
    load_ratings,
    load_links,
    load_tmdb_movies,
    load_credits,
    load_keywords,
    extract_genres
)
# Load datasets
movies = load_movies()
ratings = load_ratings()
links = load_links()

tmdb_movies = load_tmdb_movies()
credits = load_credits()
keywords = load_keywords()
"""
# Merge datasets
merged_data = merge_movies_and_ratings(movies, ratings)

# Dataset information
print("=" * 50)
print("MOVIES DATASET")
print("=" * 50)
print(movies.head())

print("\nDataset Shape:")
print(movies.shape)

print("\nColumns:")
print(movies.columns)

print("\nDataset Info:")
movies.info()

# Genres
genres = extract_genres(movies)

print("\nFirst 5 Genre Lists:")
print(genres.head())

# Missing values
print("\nMissing Values:")
print(movies.isnull().sum())

# Duplicate titles
print("\nDuplicate Titles:")
print(movies["title"].duplicated().sum())

# Longest movie title
movies["title_length"] = movies["title"].str.len()

print("\nLongest Movie Title:")
print(
    movies.loc[
        movies["title_length"].idxmax(),
        "title"
    ]
)

# Ratings dataset
print("\n" + "=" * 50)
print("RATINGS DATASET")
print("=" * 50)

print(ratings.head())

print("\nTotal Ratings:")
print(len(ratings))

print("\nUnique Users:")
print(ratings["userId"].nunique())

print("\nRated Movies:")
print(ratings["movieId"].nunique())

print("\nAverage Rating:")
print(ratings["rating"].mean())

print("\nHighest Rating:")
print(ratings["rating"].max())

print("\nLowest Rating:")
print(ratings["rating"].min())

# Merged dataset
print("\n" + "=" * 50)
print("MERGED DATASET")
print("=" * 50)

print(merged_data.head())

top_movies = top_rated_movies(merged_data)

print("\nTop Rated Movies")
print(top_movies)

print("\nGenres Column")
print(movies["genres"].head(10))
genres=extract_genres(movies)

print(extract_genres(movies).head())

genre_movies = recommend_by_genre(
    movies,
    "Comedy"
)

print("\nComedy Movies")
print(
    genre_movies[
        ["title", "genres"]
    ].head(10)
)



best_comedies = best_movies_by_genre(
    movies,
    ratings,
    "Comedy"
)

print("\nBest Comedy Movies")

print("\nAvailable Genres")

for genre in sorted(extract_genres(movies)):
    print("-", genre)

selected_genre = input("\nEnter a genre: ").strip()

recommended_movies = best_movies_by_genre(
    movies,
    ratings,
    selected_genre
)

display_movies(
    recommended_movies,
    f"Top {selected_genre} Movies"
)

print("\nMovieLens Movies")
print(movies.shape)

print("\nTMDB Movies")
print(tmdb_movies.shape)

print("\nCredits")
print(credits.shape)

print("\nKeywords")
print(keywords.shape)

print("\nTMDB Columns")
print(tmdb_movies.columns.tolist())
print("\nFirst 5 TMDB Movies")
print(tmdb_movies.head())

print("\nDataset Shape")
print(tmdb_movies.shape)

print(tmdb_movies[
    [
        "title",
        "overview",
        "genres",
        "release_date"
    ]
].head())

# Missing values
print("\nMissing Values")
print(
    tmdb_movies[
        [
            "title",
            "overview",
            "genres",
            "release_date"
        ]
    ].isnull().sum()

)
# Remove movies without overview
tmdb_movies = tmdb_movies.dropna(
    subset=["overview"]
)
# Check dataset size
print("\nDataset Shape After Cleaning")
print(tmdb_movies.shape)

tmdb_movies = tmdb_movies[
    [
        "id",
        "title",
        "overview",
        "genres",
        "release_date"
    ]
]
"""
print("\nRemaining Columns")
print(tmdb_movies.columns.tolist())

print("\nLinks Dataset")
print(links.head())

print("\nLinks Shape")
print(links.shape)

print("\nMerging MovieLens with Links...")

movies_links = movies.merge(
    links,
    on="movieId"
)

print(movies_links.head())
print("\nShape:")
print(movies_links.shape)

print("\nMerging with TMDB...")

# tmdbId sütununu sayıya çevir
print("\nTMDB Columns")
print(tmdb_movies.columns.tolist())

print("\nID Column")
print(tmdb_movies["id"].head(10))

movies_links["tmdbId"] = pd.to_numeric(
    movies_links["tmdbId"],
    errors="coerce"
)

# id sütununu sayıya çevir
tmdb_movies["id"] = pd.to_numeric(
    tmdb_movies["id"],
    errors="coerce"
)

# Sayıya çevrilemeyenleri sil
movies_links = movies_links.dropna(subset=["tmdbId"])
tmdb_movies = tmdb_movies.dropna(subset=["id"])

# Integer yap
movies_links["tmdbId"] = movies_links["tmdbId"].astype("Int64")
tmdb_movies["id"] = tmdb_movies["id"].astype("Int64")

# Merge
final_dataset = movies_links.merge(
    tmdb_movies,
    left_on="tmdbId",
    right_on="id"
)

print(final_dataset.head())

print("\nFinal Dataset Shape")
print(final_dataset.shape)