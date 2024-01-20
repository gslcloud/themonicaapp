from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models, crud
from ..database import get_db

router = APIRouter()


@router.get("/profile/{user_id}", response_model=schemas.Profile)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve profile information for a specific user

    Parameters:
    - user_id (int): ID of the user to retrieve profile for

    Returns:
    - Profile: Profile information for the specified user

    Raises:
    - HTTPException(404): If user with the specified ID is not found
    - HTTPException(500): If there is an internal server error
    """
    try:
        profile = crud.get_profile(db, user_id)
        if not profile:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/profile/{user_id}", response_model=schemas.Profile)
def update_profile(user_id: int, profile: schemas.ProfileUpdate, db: Session = Depends(get_db)):
    """
    Update profile information for a specific user

    Parameters:
    - user_id (int): ID of the user to update profile for
    - profile (ProfileUpdate): Updated profile information

    Returns:
    - Profile: Updated profile information

    Raises:
    - HTTPException(404): If user with the specified ID is not found
    - HTTPException(500): If there is an internal server error
    """
    try:
        db_profile = crud.get_profile(db, user_id)
        if not db_profile:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        updated_profile = crud.update_profile(db, db_profile, profile)
        return updated_profile
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")