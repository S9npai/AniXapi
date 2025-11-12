from fastapi import APIRouter
from controllers.favorites_controller import delete_favorite, add_new_favorite, get_user_favorites

router = APIRouter(
    tags=["Favorites"],
    prefix="/favorites"
)

router.get("/")(get_user_favorites)

router.post("/")(add_new_favorite)

router.delete("/")(delete_favorite)
