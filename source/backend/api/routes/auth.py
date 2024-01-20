from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from ..services.auth_service import AuthService, get_current_user, create_access_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

@router.post("/auth/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends()):
    user = service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/signup", response_model=dict)
async def signup(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends()):
    username = form_data.username
    password = form_data.password

    if service.is_username_taken(username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    user = service.create_user(username, password)
    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/logout")
async def logout(service: AuthService = Depends(get_current_user)):
    service.logout_user()
    return {"message": "Logged out successfully"}
