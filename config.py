from dotenv import load_dotenv
from fastapi import FastAPI
from routes import studio_routes, anime_routes, auth_routes, favorites_routes, rating_routes
from project_settings import settings

load_dotenv()

PROJECT_NAME = "AniXapi"
VERSION = "0.1.0"
DEBUG_MODE = settings.debug

app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    debug=DEBUG_MODE
)

app.include_router(studio_routes.router)
app.include_router(anime_routes.router)
app.include_router(auth_routes.router)
app.include_router(favorites_routes.router)
app.include_router(rating_routes.router)

@app.get("/")
async def root():
    return {"welcome"}

