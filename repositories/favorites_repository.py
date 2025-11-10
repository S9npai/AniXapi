from typing import Dict, Any, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.anime_model import Anime
from models.favorites_model import Favorites
import logging

logger = logging.getLogger(__name__)


class FavoritesRepository:
    def __init__(self, db:Session):
        self.db =db

    def add(self, fav_data: Dict[str, Any]) -> Favorites:
        try:
            new_fav = Favorites(**fav_data)
            self.db.add(new_fav)
            self.db.commit()
            self.db.refresh(new_fav)
            return new_fav

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error adding anime: {e}", exc_info=True)
            raise


    def get_all(self):
        return self.db.execute(
            select(Favorites).join(Favorites.anime).order_by(Anime.name)
        ).scalars().all()


    def select_anime(self, anime_name: str) -> Optional[UUID]:
        return self.db.execute(
            select(Anime.uuid).where(Anime.name == anime_name)
        ).scalar_one_or_none()


    def delete(self, user_uuid:UUID, anime_name:str) -> bool:
        anime_uuid = self.select_anime(anime_name)

        try:
            favorite_record = self.db.execute(
                select(Favorites).where(
                    Favorites.user == user_uuid,
                    Favorites.anime == anime_uuid
                )
            ).scalars().first()

            if not favorite_record:
                return False

            self.db.delete(favorite_record)
            self.db.commit()
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error removing anime favorite: {e}", exc_info=True)
            raise
