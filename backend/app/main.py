import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database import Base, engine
from backend.app.routers import auth, library, movies, recommendations


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.secret_key = os.getenv("SECRET_KEY")
    if not app.state.secret_key:
        raise RuntimeError("SECRET_KEY is not configured.")
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174",
        ).split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (movies.router, recommendations.router, auth.router, library.router):
    app.include_router(router)


@app.get("/")
def home():
    return {"message": "Welcome to CineMind API!"}
