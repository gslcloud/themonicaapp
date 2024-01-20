from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class Image(BaseModel):
    image_id: int
    name: str

class CreateImageRequest(BaseModel):
    name: str

class UpdateImageRequest(BaseModel):
    name: str

class ErrorResponse(BaseModel):
    detail: str

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/image/{image_id}")
async def get_image(image_id: int):
    # Code to handle GET request for a specific image
    return Image(image_id=image_id, name="example image")

@router.post("/image")
async def create_image(request: Request, image: CreateImageRequest):
    # Code to create a new image
    return templates.TemplateResponse("create_image.html", {"request": request, "image": image})

@router.put("/image/{image_id}")
async def update_image(image_id: int, image: UpdateImageRequest):
    # Code to update an existing image
    return Image(image_id=image_id, name=image.name)

@router.delete("/image/{image_id}")
async def delete_image(image_id: int):
    # Code to delete an image
    return {"message": f"Image with ID {image_id} deleted successfully"}

@router.exception_handler(404)
async def not_found_exception(request, exc):
    return templates.TemplateResponse("error.html", {"request": request, "error": "Page not found"})

@router.exception_handler(Exception)
async def generic_exception(request, exc):
    return ErrorResponse(detail=str(exc))