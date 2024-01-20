from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from fastapi.security import OAuth2PasswordBearer
import logging
import os

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/logout")
async def logout(request: Request, token: str = Depends(oauth2_scheme)):
    try:
        # Clear the user session
        # TODO: Implement code to clear the user session (e.g., invalidate token, delete session cookies)

        # Redirect the user to the configured logout URL
        redirect_url = os.getenv("LOGOUT_URL", "/login")  # Replace with the actual logout URL or make it configurable
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    except Exception as e:
        # Log the specific exception raised during the logout process
        logging.error(f"Error occurred during logout: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")