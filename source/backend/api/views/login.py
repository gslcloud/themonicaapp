from fastapi import APIRouter, HTTPException

from app.models.user import User
from app.schemas.token import Token
from app.utils.security import verify_password, create_access_token

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(username: str, password: str):
    user = await User.get_by_username(username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user.id)
    return {"token": token}