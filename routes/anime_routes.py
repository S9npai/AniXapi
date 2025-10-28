from typing import List
from fastapi import APIRouter
from starlette import status
from controllers.anime_controller import get_by_studio, get_all_anime, delete_anime, add_new_anime
from controllers.anime_controller import update_anime
from schemas.anime_validator import *
from schemas.studio_validator import StudioResponse

router = APIRouter(
    tags=["Anime"],
    prefix="/anime"
)

@router.post("/", response_model=AnimeResponse, status_code=status.HTTP_200_OK)
async def create_anime(anime_data: NewAnime):
    return add_new_anime(anime_data)

@router.get("/", response_model=List[AnimeResponse], status_code=status.HTTP_200_OK)
async def get_all_animes():
    return get_all_anime()

@router.patch("/{id}", response_model=AnimeResponse)
async def anime_update(anime:AnimeResponse, anime_new_data:AnimeUpdate):
    return update_anime(anime, anime_new_data)

@router.delete("/{id}")
async def del_anime(anime_to_delete:AnimeResponse):
    return delete_anime(anime_to_delete)

@router.get("/{studio}", response_model=List[AnimeResponse])
async def get_anime_by_studio(studio: StudioResponse):
    return get_by_studio(studio)

