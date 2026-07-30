import pandas as pd


def top_rated_movies(merged_data, min_votes=50, top_n=10):

    movie_stats = (
        merged_data
        .groupby("title")
        .agg(
            average_rating=("rating", "mean"),
            rating_count=("rating", "count")
        )
    )

    filtered_movies = movie_stats[
        movie_stats["rating_count"] >= min_votes
    ]

    top_movies = filtered_movies.sort_values(
        by="average_rating",
        ascending=False
    ).head(top_n)

    return top_movies

def recommend_by_genre(movies, genre):

    filtered_movies = movies[
        movies["genres"].str.contains(
            genre,
            case=False,
            na=False
        )
    ]

    return filtered_movies

def best_movies_by_genre(
    movies,
    ratings,
    genre,
    min_votes=50,
    top_n=10
):

    genre_movies = movies[
        movies["genres"].str.contains(
            genre,
            case=False,
            na=False
        )
    ]

    merged = ratings.merge(
        genre_movies,
        on="movieId"
    )

    movie_stats = (
        merged
        .groupby("title")
        .agg(
            average_rating=("rating", "mean"),
            rating_count=("rating", "count")
        )
    )

    filtered = movie_stats[
        movie_stats["rating_count"] >= min_votes
    ]

    top_movies = (
    filtered
    .sort_values(
        by=["average_rating", "rating_count"],
        ascending=[False, False]
    )
    .head(top_n)
)

    return top_movies


def display_movies(movie_dataframe, title):

    print("\n" + "=" * 45)
    print(title.upper())
    print("=" * 45)

    if movie_dataframe.empty:
        print("No movies found.")
        return

    for index, (movie_title, row) in enumerate(
        movie_dataframe.iterrows(),
        start=1
    ):

        print(f"\n{index}. {movie_title}")
        print(f"Rating : {row['average_rating']:.2f}")
        print(f"Votes  : {int(row['rating_count'])}")

        print("-" * 45)