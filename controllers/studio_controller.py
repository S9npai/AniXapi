from fastapi import Depends
from sqlalchemy.orm import Session
from repositories.studio_repository import StudioRepository
from schemas.anime_validator import AnimeResponse
from schemas.studio_validator import StudioResponse, StudioValidator, StudioUpdate
from services.studio_service import StudioService
from utils.db_connection import db_conn


def get_studio_service(db:Session = Depends(db_conn)) -> StudioService:
    repository = StudioRepository(db)
    return StudioService(repository)

def add_new_studio(new_studio_data:StudioValidator, service:StudioService = Depends(get_studio_service)):
    return service.add_studio(new_studio_data)

def get_all_studios(service:StudioService = Depends(get_studio_service)):
    return service.get_all_studios()

def update_studio(studio_requested:StudioResponse, studio_to_update:StudioUpdate, service:StudioService = Depends(get_studio_service)):
    return service.update_studio(studio_requested.uuid, studio_to_update)

def delete_studio(studio_requested: StudioResponse, service:StudioService = Depends(get_studio_service)):
    return service.delete_studio(studio_requested.uuid)

def get_studio_name(studio_name:str,  service:StudioService = Depends(get_studio_service)):
    return service.get_studio_by_name(studio_name)

def fetch_studio_by_uuid(studio_uuid:str, service:StudioService = Depends(get_studio_service)):
    return service.get_studio_by_uuid(studio_uuid)
