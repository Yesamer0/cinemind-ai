import pandas as pd

from config import (
    LINKS_PATH,
    MOVIES_PATH,
    RATINGS_PATH,
    TMDB_MOVIES_PATH,
    TMDB_CREDITS_PATH,
    TMDB_KEYWORDS_PATH
)


def load_movies():
    return pd.read_csv(MOVIES_PATH)


def load_ratings():
    return pd.read_csv(RATINGS_PATH)


def extract_genres(movies):
    return movies["genres"].str.split("|")


def merge_movies_and_ratings(movies, ratings):
    return pd.merge(
        ratings,
        movies,
        on="movieId",
        how="inner"
    )
# iki tablo alınıyor merged datada saklanıyorlar pd.merge birleştirme fonksiyonu
#  onmovieıd de iki tabloda da ortak olan movieId sütununu kullanarak eşleştir. diyor
# how="inner" = İki tabloda da bulunan kayıtları getir.
# return de birleşen tabloyu döndürüyor.
def load_tmdb_movies():
    movies = pd.read_csv(
        TMDB_MOVIES_PATH,
        low_memory=False
    )
    return movies

def load_credits():

    credits = pd.read_csv(
        TMDB_CREDITS_PATH
    )

    return credits

def load_keywords():

    keywords = pd.read_csv(
        TMDB_KEYWORDS_PATH
    )

    return keywords

def load_links():

    links = pd.read_csv(LINKS_PATH)

    return links