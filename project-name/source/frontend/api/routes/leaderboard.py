from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ..database import get_db
from ..schemas import LeaderboardEntry, EliteSushiteer
from ..models import User

router = APIRouter()

@router.get("/leaderboard", response_model=List[LeaderboardEntry], tags=["leaderboard"])
def get_leaderboard(db: Session = Depends(get_db)) -> List[LeaderboardEntry]:
    leaderboard = (
        db.query(User.username, User.donation_amount)
        .order_by(User.donation_amount.desc())
        .all()
    )
    leaderboard_data = [
        LeaderboardEntry(username=username, donation_amount=donation_amount)
        for username, donation_amount in leaderboard
    ]
    return leaderboard_data

@router.post("/leaderboard/donate/{user_id}", response_model=Dict[str, Any], tags=["leaderboard"])
def donate_to_user(user_id: int, amount: float, db: Session = Depends(get_db)) -> Dict[str, Any]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid donation amount")

    user.donation_amount += amount
    db.commit()

    return {"message": "Donation successful"}

@router.get("/leaderboard/elite-sushiteers", response_model=List[EliteSushiteer], tags=["leaderboard"])
def get_elite_sushiteers(db: Session = Depends(get_db)) -> List[EliteSushiteer]:
    elite_sushiteers = (
        db.query(User.username, User.donation_amount)
        .order_by(User.donation_amount.desc())
        .limit(3)
        .all()
    )
    elite_sushiteers_data = [
        EliteSushiteer(username=username, donation_amount=donation_amount)
        for username, donation_amount in elite_sushiteers
    ]
    return elite_sushiteers_data