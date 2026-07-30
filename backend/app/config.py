from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MOVIELENS_DIR = BASE_DIR / "dataset" / "movielens"
TMDB_DIR = BASE_DIR / "dataset" / "tmdb"

MOVIES_PATH = MOVIELENS_DIR / "movies.csv"
RATINGS_PATH = MOVIELENS_DIR / "ratings.csv"
LINKS_PATH = MOVIELENS_DIR / "links.csv"
TAGS_PATH = MOVIELENS_DIR / "tags.csv"

TMDB_MOVIES_PATH = TMDB_DIR / "movies_metadata.csv"
TMDB_CREDITS_PATH = TMDB_DIR / "credits.csv"
TMDB_KEYWORDS_PATH = TMDB_DIR / "keywords.csv"
