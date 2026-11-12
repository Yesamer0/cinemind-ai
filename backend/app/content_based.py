from functools import lru_cache
from threading import Lock

import re

from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from backend.app.data_loader import load_catalog, load_tmdb_movies


_tfidf_lock = Lock()

lemmatizer = WordNetLemmatizer()


def prepare_movies():
    movies = load_tmdb_movies()
    movies = movies.dropna(subset=["overview"])
    movies = movies[
        [
            "title",
            "overview",
            "genres"
        ]
    ]
    return movies

def create_tfidf_matrix():
    with _tfidf_lock:
        return _fit_tfidf_matrix()


@lru_cache(maxsize=1)
def _fit_tfidf_matrix():
    movies = load_catalog().copy()

    # Metinleri temizle
    movies["clean_overview"] = movies[
        "overview"
    ].apply(clean_text)

    # TF-IDF modelini oluştur
    tfidf = TfidfVectorizer(
        stop_words="english"
    )

    # TF-IDF matrisini oluştur
    tfidf_matrix = tfidf.fit_transform(
        movies["clean_overview"]
    )

    return tfidf, tfidf_matrix, movies

def recommend_movies(movie_title, top_n=5):

    tfidf, tfidf_matrix, movies = create_tfidf_matrix()

    movie_index = movies[
        movies["title"] == movie_title
    ].index

    if len(movie_index) == 0:
        return None

    movie_index = movie_index[0]

    similarity_scores = cosine_similarity(
        tfidf_matrix[movie_index],
        tfidf_matrix
    ).flatten()

    similarity_scores = list(
        enumerate(similarity_scores)
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    similarity_scores = similarity_scores[
        1:top_n+1
    ]

    recommended_movies = []

    for index, score in similarity_scores:

        movie = movies.iloc[index]

        recommended_movies.append(
            {
                "title": movie["title"],
                "similarity": score
            }
        )

    return recommended_movies


def clean_text(text):

    if not isinstance(text, str):
        return ""

    # 1. Küçük harfe çevir
    text = text.lower()

    # 2. Gereksiz karakterleri temizle
    text = re.sub(
        r"[^a-zA-Z\s]",
        "",
        text
    )

    # 3. Kelimelere ayır
    words = text.split()

    # 4. Stopwords temizle
    words = [
        word
        for word in words
        if word not in ENGLISH_STOP_WORDS
    ]

    # 5. Lemmatization
    words = [
        lemmatizer.lemmatize(word)
        for word in words
    ]

    return " ".join(words)



def recommend_by_keyword(keyword):

    tfidf, tfidf_matrix, movies = create_tfidf_matrix()

    keyword = clean_text(keyword)

    keyword_vector = tfidf.transform(
        [keyword]
    )

    similarity = cosine_similarity(
        keyword_vector,
        tfidf_matrix
    )

    similarity_scores = similarity.flatten()

    indices = similarity_scores.argsort()[::-1][:10]

    return movies.iloc[
        indices
    ][
        [
            "title",
            "overview"
        ]
    ]
