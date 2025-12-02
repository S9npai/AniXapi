import logging
from typing import Dict, Any, Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.rating_model import Rating

logger = logging.getLogger(__name__)


class RatingRepository:
    def __init__(self, db:Session):
        self.db =db


    def get_by_user_and_anime(self, user_uuid: str, anime_uuid: str) -> Optional[Rating]:
        try:
            stmt = select(Rating).where(
                Rating.user == user_uuid,
                Rating.anime == anime_uuid
            )
            return self.db.execute(stmt).scalars().first()

        except SQLAlchemyError as e:
            logger.error(f"Error fetching rating by user and anime: {e}", exc_info=True)
            raise


    def add(self, rating_data: Dict[str, Any]) -> Rating:
        try:
            new_rating = Rating(**rating_data)
            self.db.add(new_rating)
            self.db.commit()
            self.db.refresh(new_rating)
            return new_rating

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error rating anime: {e}", exc_info=True)
            raise
        
        
    def update(self, rating: Rating, update_data: Dict[str, Any]) -> Rating:
        try:
            for key, value in update_data.items():
                if hasattr(rating, key):
                    setattr(rating, key, value)

            self.db.commit()
            self.db.refresh(rating)
            return rating

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Anime rating update error !: {e}", exc_info=True)
            raise


    def delete(self, rating: Rating):
        try:
            self.db.delete(rating)
            self.db.commit()

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Anime rating deletion error !: {e}", exc_info=True)
            raise

