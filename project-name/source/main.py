from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .utils import get_statuses, update_status, get_status_count
from .database import engine, SessionLocal
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session, sessionmaker
from . import models, schemas

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency Injection for Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/profile/{username}")
def profile(request: Request, username: str):
    return templates.TemplateResponse("profile.html", {"request": request, "username": username})


@app.get("/api/statuses", response_model=List[schemas.Status])
def api_statuses(db: Session = Depends(get_db)):
    statuses = get_statuses(db)
    return statuses


@app.post("/api/statuses/update", status_code=status.HTTP_201_CREATED)
async def api_update_status(new_status: schemas.StatusCreate, db: Session = Depends(get_db)):
    try:
        update_status(db, new_status)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update status")

@app.get("/api/statuses/count", response_model=schemas.StatusCount)
def api_status_count(db: Session = Depends(get_db)):
    count = get_status_count(db)
    return {"count": count}