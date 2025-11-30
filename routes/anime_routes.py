from typing import List
from fastapi import APIRouter
from controllers.anime_controller import (
    get_all_anime, delete_anime, update_anime, get_by_studio, get_anime_by_id, anime_by_name, add_new_anime
)
from schemas.anime_validator import AnimeResponse

router = APIRouter(
    tags=["Anime"],
    prefix="/anime"
)

router.get("/", response_model=List[AnimeResponse])(get_all_anime)

router.post("/", response_model=List[AnimeResponse])(add_new_anime)

router.get("/by_studio/{studio_name}", response_model=List[AnimeResponse])(get_by_studio)

router.get("/{anime_uuid}", response_model=AnimeResponse)(get_anime_by_id)

router.get("/name/{anime_name}", response_model=AnimeResponse)(anime_by_name)

router.patch("/{anime_uuid}", response_model=AnimeResponse)(update_anime)

router.delete("/{anime_uuid}")(delete_anime)
