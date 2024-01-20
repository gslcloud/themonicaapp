from fastapi import FastAPI, Request, Cookie, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import aioredis
import sqlalchemy

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Redis connection pool
redis_pool = None


async def connect_to_redis():
    global redis_pool
    redis_pool = await aioredis.create_redis_pool("redis://localhost")


async def close_redis_connection():
    global redis_pool
    redis_pool.close()
    await redis_pool.wait_closed()


@app.on_event("startup")
async def startup():
    await connect_to_redis()


@app.on_event("shutdown")
async def shutdown():
    await close_redis_connection()


async def get_picture_url_from_database(picture_id):
    # Implement logic to fetch picture URL from the database based on picture_id
    return "https://example.com/static/pictures/" + picture_id


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    picture_id = "12345"
    picture_url = await get_picture_url_from_database(picture_id)
    return templates.TemplateResponse("index.html", {"request": request, "picture_url": picture_url})


@app.get("/profile", response_class=HTMLResponse)
async def read_profile(request: Request, session: str = Cookie(default=None)):
    if session is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    picture_id = "67890"
    picture_url = await get_picture_url_from_database(picture_id)
    return templates.TemplateResponse("profile.html", {"request": request, "picture_url": picture_url})


@app.get("/picture/{picture_id}", response_class=HTMLResponse)
async def view_picture(request: Request, picture_id: str):
    picture_url = await get_picture_url_from_database(picture_id)
    if picture_url is None:
        raise HTTPException(status_code=404, detail="Picture not found")
    return templates.TemplateResponse("picture.html", {"request": request, "picture_url": picture_url, "picture_id": picture_id})