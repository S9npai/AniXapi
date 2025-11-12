from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from models.studio_model import Studio
import logging

logger = logging.getLogger(__name__)


class StudioRepository:
    def __init__(self, db:Session):
        self.db = db


    def add(self, studio_data: Dict[str, Any]) -> Studio:
        try:
            new_studio = Studio(**studio_data)
            self.db.add(new_studio)
            self.db.commit()
            self.db.refresh(new_studio)
            return new_studio

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error adding new studio: {e}", exc_info=True)
            raise


    def get_by_name(self, name:str):
        try:
            return self.db.execute(select(Studio).where(
                Studio.name == name)
            ).scalar_one_or_none()

        except SQLAlchemyError as e:
            logger.error(f"Couldn't get studio name !: {e}", exc_info=True)
            raise


    def get_by_uuid(self, studio_uuid: str) -> Optional[Studio]:
        try:
            return self.db.execute(select(Studio).where(
                Studio.uuid == studio_uuid
            )).scalar_one_or_none()

        except SQLAlchemyError as e:
            logger.error(f"Can't get studio UUID: {e}", exc_info=True)
            raise


    def get_all(self):
        try:
            return self.db.execute(
                select(Studio).order_by(Studio.name)
            ).scalars().all()

        except SQLAlchemyError as e:
            logger.error(f"Can't get all studios: {e}", exc_info=True)
            raise


    def update(self, studio:Studio, update_data: Dict[str, Any]) -> Studio:
        try:
            for key, value in update_data.items():
                if hasattr(studio, key):
                    setattr(studio, key, value)

            self.db.commit()
            self.db.refresh(studio)
            return studio

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Studio update error !: {e}", exc_info=True)
            raise


    def delete(self, studio_uuid:str) -> bool:
        try:
            studio = self.get_by_uuid(studio_uuid)
            if not studio:
                return False

            self.db.delete(studio)
            self.db.commit()
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error deleting studio record !:{e}", exc_info=True)
            return False

