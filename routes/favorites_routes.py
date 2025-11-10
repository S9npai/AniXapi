from fastapi import APIRouter
from controllers.favorites_controller import get_all_favorites, delete_favorite, add_new_favorite

router = APIRouter(
    tags=["Favorites"],
    prefix="/favorites"
)

router.get("/")(get_all_favorites)

router.post("/")(add_new_favorite)

router.delete("/")(delete_favorite)
