from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc
from fastapi.responses import JSONResponse
from typing import List

from ..database import get_session
from ..models import User
from ..dependencies import get_db_session

router = APIRouter()


@router.get("/api/wavers/recent", response_model=List[str])
async def get_recent_wavers(session=Depends(get_db_session)):
    try:
        query = select(User.username).order_by(desc(User.clicked_at)).limit(10)
        result = await session.execute(query)
        recent_wavers = [row[0] for row in result]
        return recent_wavers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))