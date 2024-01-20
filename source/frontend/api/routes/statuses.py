from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Status, StatusCreate, StatusResponse

router = APIRouter()


@router.get("/statuses", response_model=list[StatusResponse])
async def get_statuses(db: Session = Depends(get_db)):
    statuses = db.query(Status).all()
    return [StatusResponse(id=status.id, content=status.content, favorites=status.favorites) for status in statuses]


@router.post("/statuses", response_model=StatusResponse)
async def create_status(status: StatusCreate, db: Session = Depends(get_db)):
    new_status = Status(content=status.content, favorites=0)
    db.add(new_status)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=422, detail="Status already exists")
    except DataError:
        db.rollback()
        raise HTTPException(status_code=422, detail="Invalid data provided for status")
    db.refresh(new_status)
    return StatusResponse(id=new_status.id, content=new_status.content, favorites=new_status.favorites)


@router.patch("/statuses/{status_id}/favorite", response_model=StatusResponse)
async def favorite_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(Status).get(status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    status.favorites += 1
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update favorites count")
    return StatusResponse(id=status.id, content=status.content, favorites=status.favorites)