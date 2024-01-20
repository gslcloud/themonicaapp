from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..security import authenticate, authorize

router = APIRouter()
security = HTTPBearer()


@router.get("/leaderboard", response_model=List[schemas.LeaderboardResponse])
def get_leaderboard(db: Session = Depends(get_db), current_user: models.User = Depends(security)):
    """
    Retrieve the top three donors and return the leaderboard data
    """
    if not authenticate(current_user.username, current_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not authorize(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You must have gifted sushi to access the leaderboard")

    top_donors = db.query(models.Donor).order_by(models.Donor.amount_donated.desc()).limit(3).all()

    leaderboard_data = []
    for donor in top_donors:
        leaderboard_data.append(schemas.LeaderboardResponse(username=donor.user.username, amount_donated=donor.amount_donated))

    return leaderboard_data