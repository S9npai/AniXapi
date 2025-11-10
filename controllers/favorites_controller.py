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

def get_all_favorites(service:FavoritesService = Depends(get_favorites_service)):
    return service.get_all_favorites()

def delete_favorite(user:UUID4, fav_requested:str, service:FavoritesService = Depends(get_favorites_service)):
    return service.delete_favorite(user, fav_requested)

