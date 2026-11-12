from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
ALGORITHM = "HS256"
ACCESS_TOKEN_TTL = timedelta(hours=1)

router = APIRouter()


@router.post("/register")
def register_user(
    username: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        (User.username == username) |
        (User.email == email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    hashed_password = pwd_context.hash(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "username": new_user.username
    }


@router.post("/login")
def login_user(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    if not pwd_context.verify(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    token = jwt.encode(
        {
            "sub": str(user.id),
            "username": user.username,
            "exp": datetime.now(timezone.utc) + ACCESS_TOKEN_TTL,
        },
        request.app.state.secret_key,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:

        payload = jwt.decode(
            token,
            request.app.state.secret_key,
            algorithms=[ALGORITHM],
            options={"require_exp": True},
        )

        user_id = int(payload["sub"])

    except (JWTError, KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user
