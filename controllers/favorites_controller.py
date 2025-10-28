from typing import List

from sqlalchemy import and_
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from models.anime_model import Anime
from models.favorites_model import Favorites
from schemas.favorites_validator import FavoritesValidator
from utils.uuid_conv import uuid_to_binary


def add_to_favorites(db: Session, user_id: str, anime_id: str) -> FavoritesValidator:
    result = db.execute(
        update(Favorites).where((Favorites.user == user_id) &
        (Favorites.anime == anime_id)))

    try:
        new_favorite = Favorites(user=user_id, anime=anime_id)
        db.add(new_favorite)
        db.commit()
        db.refresh(new_favorite)

        return FavoritesValidator.model_validate(new_favorite)

    except (IntegrityError, Exception):
        db.rollback()
        return {"status": "error", "message": "Invalid user or anime UUIDs"}, 400


def delete_from_favorites(db: Session, user_uuid: str, anime_uuid: str) -> None:
    anime_to_remove = db.query(Favorites).get((user_uuid, anime_uuid))

    if not anime_to_remove:
        raise Exception("Rating not found.")

    db.commit()


def get_favorites(db:Session, user_uuid: str, anime_uuid: str) -> list[FavoritesValidator] | tuple[None, str]:
    binary_user_uuid = uuid_to_binary(user_uuid)
    binary_anime_uuid = uuid_to_binary(anime_uuid)

    favorites = db.execute(
        select(Favorites).where(
            and_ (Favorites.user == binary_user_uuid,
                  Favorites.anime == binary_anime_uuid)
        ).order_by(Anime.name)
    ).scalars().all()

    if not favorites:
        return None, "The user has no favorite anime !"

    return [FavoritesValidator.model_validate(f) for f in favorites]

