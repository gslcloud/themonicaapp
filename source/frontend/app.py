from fastapi import FastAPI, APIRouter, Request
from starlette.responses import JSONResponse, HTMLResponse, FileResponse
import jinja2

# Create the FastAPI instance
app = FastAPI()

# Create an API router
api_router = APIRouter()

# Template environment setup
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

# Route for home page
@api_router.get("/")
async def home(request: Request) -> HTMLResponse:
    template = template_env.get_template("home.html")
    return HTMLResponse(template.render())

# API route for sushi gift
@api_router.post("/api/sushi/gift")
async def sushi_gift(request: Request) -> JSONResponse:
    # TODO: Implement sushi gift logic
    return JSONResponse({"message": "Sushi gift received"})

# API route for retrieving user profile
@api_router.get("/api/profile/{username}")
async def get_user_profile(request: Request, username: str) -> HTMLResponse:
    # TODO: Implement user profile retrieval logic
    template = template_env.get_template("profile.html")
    return HTMLResponse(template.render(username=username))

# Route for serving static files
@app.get("/static/{filename}")
async def static_file(filename: str) -> FileResponse:
    return FileResponse(f"static/{filename}")

# Mount the API router to the app
app.include_router(api_router)
