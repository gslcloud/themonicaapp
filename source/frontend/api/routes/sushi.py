from fastapi import FastAPI, Form, Query, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi import FastAPI, Form, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi import Query
from fastapi.middleware.static import StaticFiles
from fastapi import FastAPI, Form, Query

from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return {"detail": exc.errors(), "body": exc.body}


@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    return {"detail": exc.detail}


class SushiGiftRequest(BaseModel):
    sushi_type: str
    quantity: int

class SushiGiftRequest(BaseModel):
    sushi_type: str
    quantity: int


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {})


@app.get("/monica", response_class=HTMLResponse)
async def monica_profile(request: Request):
    return templates.TemplateResponse("monica_profile.html", {})


@app.post("/gift-sushi")
async def gift_sushi(request: Request, sushi_gift: SushiGiftRequest = Form(...)):
    # Process the sushi gift request, make API calls to Stripe integration, and update the database with donation details
    # Return an appropriate response to indicate the success or failure of the donation
    pass

@app.get("/elite-sushiteers", response_class=HTMLResponse)
async def elite_sushiteers(request: Request):
    return templates.TemplateResponse("secret.html", {})