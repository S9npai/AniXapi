from fastapi import Depends
from sqlalchemy.orm import Session
from repositories.anime_repository import AnimeRepository
from schemas.anime_validator import NewAnime, AnimeUpdate, AnimeResponse
from schemas.studio_validator import StudioResponse, StudioValidator
from services.anime_service import AnimeService
from utils.db_connection import db_conn


def get_anime_service(db:Session = Depends(db_conn)) -> AnimeService:
    repository = AnimeRepository(db)
    return AnimeService(repository)

def add_new_anime(new_anime_data:NewAnime, service:AnimeService = Depends(get_anime_service)):
    return service.add_new_anime(new_anime_data)

def get_all_anime(service:AnimeService = Depends(get_anime_service)):
    return service.get_all_anime()

def update_anime(anime_requested:AnimeResponse, anime_to_update:AnimeUpdate, service:AnimeService = Depends(get_anime_service)):
    return service.update_anime(anime_requested.uuid, anime_to_update)

def delete_anime(anime_requested: AnimeResponse, service:AnimeService = Depends(get_anime_service)):
    return service.delete_anime(anime_requested.uuid)

def get_by_studio(studio_uuid:str, service:AnimeService = Depends(get_anime_service)):
    return service.get_anime_by_studio(studio_uuid)

def get_anime_by_id(anime_uuid:str, service:AnimeService = Depends(get_anime_service)):
    return service.get_anime_by_uuid(anime_uuid)
