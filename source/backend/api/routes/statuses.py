from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal
from ..models import Status
from .. import my_custom_functions

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/statuses/all", response_model=List[Status])
def get_statuses(db: Session = Depends(get_db)):
    statuses = my_custom_functions.get_statuses_from_db(db)
    return statuses


@router.post("/statuses/favorite/{status_id}")
def favorite_status(status_id: int, db: Session = Depends(get_db)):
    status = my_custom_functions.get_status_from_db(db, status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")

    try:
        status.favorite_count += 1
        db.commit()
        db.refresh(status)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while updating the status") from e

    return {"message": "Status is favorited", "status_id": status_id}