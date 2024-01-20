from fastapi import APIRouter, Request, Depends, HTTPException, Header
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from .templates import templates
from .schemas import Status
from .database import SessionLocal, engine
from .models import Base, Status as StatusModel

import redis

router = APIRouter()

# Initialize Redis connection
redis_host = 'localhost'
redis_port = 6379
try:
    redis_db = redis.Redis(host=redis_host, port=redis_port)
except Exception as e:
    print(f"Failed to connect to Redis: {e}")
    raise e
    

# Initialize SQLAlchemy database session
Base.metadata.create_all(bind=engine)
try:
    db = SessionLocal()
except Exception as e:
    print(f"Failed to connect to database: {e}")
    raise e


@router.get("/profile", response_class=HTMLResponse)
async def get_profile(request: Request, x_requested_with: str = Header(None)):
    if x_requested_with == 'XMLHttpRequest':
        return JSONResponse(content=request.app.profile_data)
    else:
        return templates.TemplateResponse("profile.html", {"request": request, "profile": request.app.profile_data})


@router.get("/api/profile", response_model=List[Status])
async def get_status():
    return request.app.profile_data


@router.post("/api/profile/status")
async def add_status(status: Status, db: Session = Depends(get_db)):
    new_status = StatusModel(status=status.status, favorites=status.favorites)
    db.add(new_status)
    db.commit()
    db.refresh(new_status)
    return JSONResponse(content={"message": "Status added successfully"})


@router.post("/api/profile/status/{status_id}/like")
async def like_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(StatusModel).filter(StatusModel.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    status.favorites += 1
    db.commit()
    return JSONResponse(content=status.favorites)


@router.post("/api/profile/status/{status_id}/neko")
async def neko_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(StatusModel).filter(StatusModel.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return JSONResponse(content=f"Maneki Neko interaction with status {status_id}")


async def update_profile_data():
    # Fetch profile data from the API
    response = await client.get("/api/profile")
    profile_data = await response.json()
    app.profile_data = profile_data


@app.on_event("startup")
async def startup_event():
    app.profile_data = []
    await update_profile_data()


@app.on_event("shutdown")
async def shutdown_event():
    app.profile_data = None