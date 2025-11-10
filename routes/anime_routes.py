from typing import List
from fastapi import APIRouter
from controllers.anime_controller import get_all_anime, delete_anime, add_new_anime, update_anime, get_by_studio, \
    get_anime_by_id
from schemas.anime_validator import *

router = APIRouter(
    tags=["Anime"],
    prefix="/anime"
)

router.post("/", response_model=AnimeResponse)(add_new_anime)

router.get("/all", response_model=List[AnimeResponse])(get_all_anime)

router.patch("/", response_model=AnimeResponse)(update_anime)

router.delete("/")(delete_anime)

router.get("/by_studio/{studio}", response_model=List[AnimeResponse])(get_by_studio)

router.get("/{uuid}", response_model=AnimeResponse)(get_anime_by_id)

