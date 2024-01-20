from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.models import User
from app.token import create_access_token, verify_password
from app.config import settings

router = APIRouter()

# JWT related constants
ALGORITHM = "HS256"
SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def authenticate_user(username: str, password: str) -> Optional[User]:
    user = User.get_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_token(user: User) -> str:
    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        "sub": user.username,
        "exp": expiration_time
    }
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


@router.post("/login")
def login(username: str = Body(...), password: str = Body(...)):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_token(user)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")


@router.get("/users/{username}")
def get_user(username: str):
    user = User.get_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username}

