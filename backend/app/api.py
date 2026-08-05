from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.app.semantic_search import semantic_search, movies
# Create the FastAPI application instance
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to CineMind API!"
    }

# Search endpoint
@app.get("/search")
def search_movies(
    query: str = Query(..., min_length=2, description="Movie search query"),
    limit: int = Query(5, ge=1, le=20)
):
    results = semantic_search(query, top_n=limit)

    return {
        "query": query,
        "total_results": len(results),
        "results": results
    }


@app.get("/movies")
def get_movies(
    limit: int = 20,
    offset: int = 0,
    sort: str = "id"
):

    if sort == "title":
        sorted_movies = movies.sort_values("title")
    else:
        sorted_movies = movies

    results = []

    end = offset + limit

    for i in range(offset, min(end, len(sorted_movies))):

        movie = sorted_movies.iloc[i]

        results.append({
            "id": i,
            "title": movie["title"],
            "overview": movie["overview"]
        })

    return results
# Return the first 10 movies when the application starts.
@app.get("/popular")
def popular_movies():

    results = []

    for i in range(10):

        movie = movies.iloc[i]

        results.append({
            "id": i,
            "title": movie["title"],
            "overview": movie["overview"]
        })

    return results