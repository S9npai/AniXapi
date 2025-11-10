from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from models.studio_model import Studio
from repositories.base_repository import BaseRepository


class StudioRepository(BaseRepository[Studio]):
    def __init__(self, db:Session):
        self.db = db

    def get_all(self):
        return self.db.execute(
            select(Studio).order_by(Studio.name)
        ).scalars().all()

    def add(self, studio_data: Dict[str, Any]) -> Studio:
        new_studio = Studio(**studio_data)
        self.db.add(new_studio)
        self.db.commit()
        self.db.refresh(new_studio)
        return new_studio

    def delete(self, uuid: str) -> bool:
        try:
            studio = self.get_by_uuid(uuid)
            if not studio:
                return False

            self.db.delete(studio)
            self.db.commit()
            return True

        except SQLAlchemyError:
            self.db.rollback()
            return False

    def get_by_name(self, name:str):
        return self.db.execute(select(Studio).where(
            Studio.name == name)
        ).scalar_one_or_none()

    def get_by_uuid(self, studio_uuid: str) -> Optional[Studio]:
        return self.db.execute(select(Studio).where(
            Studio.uuid == studio_uuid
        )).scalar_one_or_none()

    def update(self, studio: Studio, update_data: Dict[str, Any]) -> Studio:
        for key, value in update_data.items():
            if hasattr(studio, key):
                setattr(studio, key, value)

        self.db.commit()
        self.db.refresh(studio)
        return studio