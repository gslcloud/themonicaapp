from fastapi import FastAPI, Request, Depends, HTTPException, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from pydantic import BaseModel
from passlib.hash import bcrypt

# Database Configuration
engine = create_engine('sqlite:///database.db')
SessionLocal = sessionmaker(bind=engine)

# FastAPI App
app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Dependency Injection for Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Models
class User(BaseModel):
    username: str
    password: str


# Routes
@app.get("/")
def home(request: Request, username: str = Depends(get_db)):
    return templates.TemplateResponse("home.html", {"request": request, "username": username})


@app.get("/register")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
def register(user: User, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = bcrypt.hash(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    
    return RedirectResponse(url="/", status_code=201)


@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(user: User, db: Session = Depends(get_db), response: Response = Depends(get_db)):
    user_db = db.query(User).filter(User.username == user.username).first()
    if not user_db or not bcrypt.verify(user.password, user_db.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    response.set_cookie(key="username", value=user.username)
    return RedirectResponse(url="/")


@app.get("/logout")
def logout(response: Response):
    response.delete_cookie(key="username")
    return RedirectResponse(url="/")