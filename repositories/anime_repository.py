from typing import List, Dict, Any, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.anime_model import Anime
from repositories.base_repository import BaseRepository
from utils.uuid_conv import uuid_to_binary


class AnimeRepository(BaseRepository[Anime]):
    def __init__(self, db: Session):
        self.db = db

    def add(self, anime_data: Dict[str, Any]) -> Anime:
        try:
            new_anime = Anime(**anime_data)
            self.db.add(new_anime)
            self.db.commit()
            self.db.refresh(new_anime)
            return new_anime
        except SQLAlchemyError:
            self.db.rollback()

    def get_by_uuid(self, anime_uuid: str) -> Optional[Anime]:
        binary_uuid = uuid_to_binary(anime_uuid)
        return self.db.execute(
            select(Anime).where(Anime.uuid == binary_uuid)
        ).scalar_one_or_none()

    def get_all(self):
        return self.db.execute(
            select(Anime).order_by(Anime.name)
        ).scalars().all()

    def update(self, anime:Anime, update_data:Dict[str, Any]) -> Anime:
        try:
            for key, value in update_data.items():
                if hasattr(anime, key):
                    setattr(anime, key, value)

            self.db.commit()
            self.db.refresh(anime)
            return anime

        except SQLAlchemyError:
            self.db.rollback()

    def delete(self, anime_uuid: str) -> bool:
        try:
            anime = self.get_by_uuid(anime_uuid)
            if not anime:
                return False

            self.db.delete(anime)
            self.db.commit()
            return True

        except SQLAlchemyError:
            self.db.rollback()

    def get_by_name(self, name: str) -> Optional[Anime]:
        return self.db.execute(
            select(Anime).where(Anime.name == name)
        ).scalar_one_or_none()

    def get_by_studio(self, studio_uuid: str):
        return self.db.execute(
            select(Anime).where(Anime.studio == studio_uuid)
        ).scalars().all()

