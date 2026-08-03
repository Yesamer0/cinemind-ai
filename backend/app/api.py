from fastapi import FastAPI
from backend.app.semantic_search import semantic_search

# Create the FastAPI application instance
app = FastAPI()


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to CineMind API!"
    }

# Search endpoint
@app.get("/search")
def search_movies(query: str):

    results = semantic_search(query)

    return {
        "query": query,
        "results": results
}