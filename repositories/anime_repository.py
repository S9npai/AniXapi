from typing import Dict, Any, Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.anime_model import Anime
from models.studio_model import Studio
import logging

logger = logging.getLogger(__name__)


class AnimeRepository:
    def __init__(self, db:Session):
        self.db = db


    def add(self, anime_data: Dict[str, Any]) -> Anime:
        try:
            new_anime = Anime(**anime_data)
            self.db.add(new_anime)
            self.db.commit()
            self.db.refresh(new_anime)
            return new_anime

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error adding anime: {e}", exc_info=True)
            raise


    def get_by_uuid(self, anime_uuid: str) -> Optional[Anime]:
        try:
            return self.db.execute(
                select(Anime).where(Anime.uuid == anime_uuid)
            ).scalar_one_or_none()

        except SQLAlchemyError as e:
            logger.error(f"Error getting anime UUID: {e}", exc_info=True)
            raise


    def get_all(self):
        try:
            return self.db.execute(
                select(Anime).order_by(Anime.name)
            ).scalars().all()

        except SQLAlchemyError as e:
            logger.error(f"Couldn't fetch all anime !: {e}", exc_info=True)
            raise


    def get_by_name(self, name: str) -> Optional[Anime]:
        try:
            return self.db.execute(
                select(Anime).where(Anime.name == name)
            ).scalar_one_or_none()

        except SQLAlchemyError as e:
            logger.error(f"Error querying anime name: {e}", exc_info=True)
            raise


    def get_by_studio(self, studio_name: str):
        try:
            return self.db.execute(
                select(Anime)
                .join(Anime.studios)
                .where(Studio.name == studio_name)
                .group_by(Anime.uuid)
            ).scalars().all()

        except SQLAlchemyError as e:
            logger.error(f"Error getting anime by studio: {e}", exc_info=True)
            raise


    def update(self, anime:Anime, update_data:Dict[str, Any]):
        try:
            for key, value in update_data.items():
                if hasattr(anime, key):
                    setattr(anime, key, value)

            self.db.commit()
            self.db.refresh(anime)
            return anime

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Anime update error !: {e}", exc_info=True)
            raise


    def delete(self, anime_uuid: str):
        try:
            anime = self.get_by_uuid(anime_uuid)
            if not anime:
                return False

            self.db.delete(anime)
            self.db.commit()
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error deleting anime record: {e}", exc_info=True)
            return False

