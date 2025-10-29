from fastapi import APIRouter, FastAPI, Depends
from sqlalchemy.orm.session import Session
from controllers.favorites_controller import delete_from_favorites, add_to_favorites
from schemas.anime_validator import AnimeResponse
from schemas.auth_validator import UserResponse
from schemas.favorites_validator import FavoritesValidator
from utils.db_connection import *
from middleware.auth import *

router = APIRouter(
    tags=["Favorites"],
    prefix="/favorites"
)

@router.post("/")
async def add_fav(user:UserResponse.uuid, anime:AnimeResponse.uuid, db: Session = Depends(db_conn)):
    return add_to_favorites(db, user, anime)

@router.delete("/", )
async def del_fav(user:UserResponse.uuid, anime:AnimeResponse.uuid, db: Session = Depends(db_conn)):
    return delete_from_favorites(db, user, anime)

