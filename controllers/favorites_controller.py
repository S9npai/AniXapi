from fastapi import Depends
from pydantic import UUID4
from sqlalchemy.orm import Session
from repositories.favorites_repository import FavoritesRepository
from schemas.favorites_validator import FavoritesValidator
from services.favorites_service import FavoritesService
from utils.db_connection import db_conn


def get_favorites_service(db:Session = Depends(db_conn)) -> FavoritesService:
    repository = FavoritesRepository(db)
    return FavoritesService(repository)

def add_new_favorite(new_fav_data:FavoritesValidator, service:FavoritesService = Depends(get_favorites_service)):
    return service.add_new_favorite(new_fav_data)

def get_user_favorites(user_uuid:str, service:FavoritesService = Depends(get_favorites_service)):
    return service.get_user_favs(user_uuid)

def delete_favorite(user_uuid:UUID4, anime_uuid:UUID4, service:FavoritesService = Depends(get_favorites_service)):
    return service.delete_favorite(str(user_uuid), str(anime_uuid))

