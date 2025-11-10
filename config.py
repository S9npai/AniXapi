import os
from dotenv import load_dotenv
from fastapi import FastAPI
from routes import studio_routes, anime_routes

load_dotenv()

PROJECT_NAME = "AniXapi"
VERSION = "1.0.0"
DEBUG_MODE = os.getenv("DEBUG MODE", "True").lower() == "true"

app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    debug=DEBUG_MODE
)

app.include_router(studio_routes.router)
app.include_router(anime_routes.router)

@app.get("/")
async def root():
    return {"welcome"}

