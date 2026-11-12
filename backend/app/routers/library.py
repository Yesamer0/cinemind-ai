from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import Favorite, Rating, User
from backend.app.routers.auth import get_current_user

router = APIRouter()


@router.post("/favorites/{movie_id}")
def add_favorite(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing_favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.movie_id == movie_id
    ).first()

    if existing_favorite:
        raise HTTPException(
            status_code=400,
            detail="Movie already in favorites"
        )

    favorite = Favorite(
        user_id=current_user.id,
        movie_id=movie_id
    )

    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return {
        "message": "Movie added to favorites",
        "movie_id": movie_id
    }



@router.get("/favorites")
def get_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    favorites = db.query(Favorite).filter(
        Favorite.user_id == current_user.id
    ).all()

    return [
        {
            "movie_id": favorite.movie_id
        }
        for favorite in favorites
    ]


@router.delete("/favorites/{movie_id}")
def remove_favorite(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.movie_id == movie_id
    ).first()

    if favorite is None:
        raise HTTPException(
            status_code=404,
            detail="Movie is not in favorites"
        )

    db.delete(favorite)
    db.commit()

    return {
        "message": "Movie removed from favorites",
        "movie_id": movie_id
    }


@router.post("/ratings/{movie_id}")
def rate_movie(
    movie_id: int,
    rating: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if rating < 1 or rating > 5:
        raise HTTPException(
            status_code=400,
            detail="Rating must be between 1 and 5"
        )

    existing_rating = db.query(Rating).filter(
        Rating.user_id == current_user.id,
        Rating.movie_id == movie_id
    ).first()

    if existing_rating:

        existing_rating.rating = rating

    else:

        new_rating = Rating(
            user_id=current_user.id,
            movie_id=movie_id,
            rating=rating
        )

        db.add(new_rating)

    db.commit()

    return {
        "message": "Movie rated successfully",
        "movie_id": movie_id,
        "rating": rating
    }


@router.get("/ratings/{movie_id}")
def get_movie_rating(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    rating = db.query(Rating).filter(
        Rating.user_id == current_user.id,
        Rating.movie_id == movie_id
    ).first()

    if rating is None:

        return {
            "movie_id": movie_id,
            "rating": None
        }

    return {
        "movie_id": movie_id,
        "rating": rating.rating
    }
