from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Create the FastAPI app
app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Define the home route
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Define the profile route
@app.get("/profile/{user_id}")
def profile(request: Request, user_id: int):
    return templates.TemplateResponse("profile.html", {"request": request, "user_id": user_id})

# Define the sushi gifting route
@app.post("/sushigift")
def sushi_gift(request: Request, profile_id: int):
    # TODO: Implement sushi gift logic
    return {"message": f"Sushi gifted to profile with ID {profile_id}"}

# Define the like status route
@app.post("/likestatus")
def like_status(request: Request, status_id: int):
    # TODO: Implement like status logic
    return {"message": f"Status with ID {status_id} liked"}

# Define the Maneki Neko interaction route
@app.post("/manekinekointeraction")
def maneki_neko_interaction(request: Request):
    # TODO: Implement Maneki Neko interaction logic
    return {"message": "Maneki Neko interacted"}

# Define the Stripe webhook route
@app.post("/stripe-webhook")
def stripe_webhook(request: Request):
    # TODO: Implement Stripe webhook logic
    return {}
