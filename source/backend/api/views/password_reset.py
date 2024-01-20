from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter import FastAPILimiter, RateLimiter
from pydantic import BaseModel, EmailStr
from typing import Dict

router = APIRouter()

# Rate limiting configuration
limiter = RateLimiter()
FastAPILimiter.init(config=[limiter])

class ResetPasswordRequest(BaseModel):
    email: EmailStr

@router.post("/password/reset")
@FastAPILimiter.limit(limiter)
async def reset_password(request: ResetPasswordRequest, db: Database = Depends(get_db)):
    try:
        email = request.email

        # Perform database operations to retrieve user by email and save the reset token
        user = db.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with email {email} not found")

        reset_token = secrets.token_urlsafe(64)
        db.save_reset_token(email, reset_token)

        # Send the password reset email
        send_reset_email(email, reset_token)

        return {"message": "Password reset email has been sent", "reset_token": reset_token}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e