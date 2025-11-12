from fastapi import Depends
from sqlalchemy.orm import Session
from repositories.anime_repository import AnimeRepository
from repositories.studio_repository import StudioRepository
from schemas.anime_validator import NewAnime, AnimeUpdate
from services.anime_service import AnimeService
from utils.db_connection import db_conn


def get_anime_service(db:Session = Depends(db_conn)) -> AnimeService:
    anime_repo = AnimeRepository(db)
    studio_repo = StudioRepository(db)
    return AnimeService(anime_repo, studio_repo)

def add_new_anime(new_anime_data:NewAnime, service:AnimeService = Depends(get_anime_service)):
    return service.add_new_anime(new_anime_data)

def get_all_anime(service:AnimeService = Depends(get_anime_service)):
    return service.get_all_anime()

def get_by_studio(studio_name:str, service:AnimeService = Depends(get_anime_service)):
    return service.get_anime_by_studio(studio_name)

def get_anime_by_id(anime_uuid:str, service:AnimeService = Depends(get_anime_service)):
    return service.get_anime_by_uuid(anime_uuid)

def anime_by_name(anime_name:str, service:AnimeService = Depends(get_anime_service)):
    return service.get_anime_by_name(anime_name)

def update_anime(anime_uuid:str, anime_to_update:AnimeUpdate, service:AnimeService = Depends(get_anime_service)):
    return service.update_anime(anime_uuid, anime_to_update)

def delete_anime(anime_uuid:str, service:AnimeService = Depends(get_anime_service)):
    return service.delete_anime(anime_uuid)

