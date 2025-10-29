from typing import List
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from models.anime_model import Anime
from models.favorites_model import Favorites
from schemas.favorites_validator import FavoritesValidator
from utils.uuid_conv import uuid_to_binary


def add_to_favorites(db: Session, user_id: str, anime_id: str) -> FavoritesValidator | tuple[dict[str, str], int]:
    binary_user_id = uuid_to_binary(user_id)
    binary_anime_id = uuid_to_binary(anime_id)

    try:
        new_favorite = Favorites(user=binary_user_id, anime=binary_anime_id)
        db.add(new_favorite)
        db.commit()
        db.refresh(new_favorite)

        return FavoritesValidator.model_validate(new_favorite)

    except (IntegrityError, Exception):
        db.rollback()
        return {"status": "error", "message": "Invalid user or anime UUIDs"}, 400


def delete_from_favorites(db: Session, user_uuid: str, anime_uuid: str) -> None:
    binary_user_id = uuid_to_binary(user_uuid)
    binary_anime_id = uuid_to_binary(anime_uuid)

    anime_to_remove = db.query(Favorites).get((binary_user_id, binary_anime_id))

    if not anime_to_remove:
        raise HTTPException(
            status_code=404,
            detail="Anime favorite not found for this user !"
        )

    try:
        db.delete(anime_to_remove)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Could not delete favorite: {e}"
        )


def get_favorites(db:Session, user_uuid: str) -> list[FavoritesValidator] | tuple[None, str]:
    binary_user_uuid = uuid_to_binary(user_uuid)

    favorites = db.execute(select(Favorites).where(Favorites.user == binary_user_uuid).order_by(Anime.name)).scalars().all()

    if not favorites:
        return None, "The user has no favorite anime !"

    return [FavoritesValidator.model_validate(f) for f in favorites]

