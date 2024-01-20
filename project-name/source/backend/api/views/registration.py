from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, constr, EmailStr
from bcrypt import hashpw, gensalt
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import stripe

router = APIRouter()

stripe.api_key = "your_stripe_api_key"

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True)
    password = Column(String)
    username = Column(String)
    profile_picture = Column(String, nullable=True)


class UserIn(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    username: constr(min_length=3)
    profile_picture: str = None


engine = create_engine("sqlite:///users.db")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_user(session, user_data):
    user = User(
        email=user_data.email,
        password=user_data.password,
        username=user_data.username,
        profile_picture=user_data.profile_picture,
    )
    session.add(user)
    session.commit()


@router.post("/register")
def register(user_data: UserIn):
    session = SessionLocal()

    # Check if email is already registered
    if session.query(User).filter_by(email=user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    email = user_data.email
    password = user_data.password

    # Validate email format
    # ... (add email validation logic here)

    # Validate password strength
    # ... (add password validation logic here)

    # Hash the password
    hashed_password = hashpw(password.encode(), gensalt())

    # Create user and add to the database
    create_user(session, UserIn(email=email, password=hashed_password, username=user_data.username, profile_picture=user_data.profile_picture))

    # Handle stripe payment
    try:
        stripe.PaymentIntent.create(
            amount=1000,  # amount in cents
            currency="usd",
            description="Account Registration",
            source=user_data.stripe_token,
        )
    except stripe.error.CardError as e:
        raise HTTPException(status_code=400, detail=f"Card error: {e}")
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=f"Stripe error: {e}")

    return {"message": "User registered successfully"}