from typing import List
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import select
from models.studio_model import Studio
from repositories.anime_repository import AnimeRepository
from schemas.anime_validator import NewAnime, AnimeResponse, AnimeUpdate


class AnimeService:
    def __init__(self, repository:AnimeRepository):
        self.repository = repository

    def add_new_anime(self, anime_data:NewAnime) -> AnimeResponse:
        anime_dict = anime_data.model_dump()
        anime_uuid = str(uuid4())
        anime_dict["uuid"] = anime_uuid
        studio_uuid_str = anime_dict.pop("studio_uuid")
        anime_dict["studio"] = studio_uuid_str

        studio = self.repository.db.execute(
            select(Studio).where(Studio.uuid == studio_uuid_str)
        ).scalar_one_or_none()
        if not studio:
            raise HTTPException(status_code=404, detail="Studio doesn't exist")

        try:
            new_anime = self.repository.add(anime_dict)
            return AnimeResponse.model_validate(new_anime)

        except IntegrityError:
            raise HTTPException(status_code=400, detail="Integrity error !")

    def get_all_anime(self) -> List[AnimeResponse]:
        animes = self.repository.get_all()
        return [AnimeResponse.model_validate(a) for a in animes]

    def delete_anime(self, anime_uuid:str) -> bool:
        return self.repository.delete(anime_uuid)

    def update_anime(self, anime_uuid:str, anime_update:AnimeUpdate) -> AnimeResponse:
        existing_anime = self.repository.get_by_uuid(anime_uuid)
        if not existing_anime:
            raise HTTPException(status_code=404, detail=f"Anime with UUID '{anime_uuid}' not found.")

        update_data = anime_update.model_dump(exclude_unset=True)

        studio_updated = False

        if "studio_name" in update_data:
            studio_name = update_data.pop("studio_name")
            studio = self.repository.db.execute(select(Studio).where(Studio.name == studio_name)).scalar_one_or_none()
            if not studio:
                raise HTTPException(status_code=404, detail="Anime Studio provided for update does not exist")
            update_data["studio"] = studio.uuid
            studio_updated = True

        elif "studio_uuid" in update_data:
            studio_uuid_str = update_data.pop("studio_uuid")
            studio = self.repository.db.execute(
                select(Studio).where(Studio.uuid == studio_uuid_str)
            ).scalar_one_or_none()
            if not studio:
                raise HTTPException(status_code=404, detail="Anime Studio provided for update does not exist")
            update_data["studio"] = studio_uuid_str
            studio_updated = True

        start_date = update_data.get("start_date", existing_anime.start_date)
        end_date = update_data.get("end_date", existing_anime.end_date)
        if start_date and end_date and start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date cannot come after end date!")

        try:
            updated_anime = self.repository.update(existing_anime, update_data)
            return AnimeResponse.model_validate(updated_anime)

        except IntegrityError:
            raise HTTPException(status_code=400, detail="Database integrity error during anime update")

    def get_anime_by_studio(self, studio_uuid:str):
        studio_animes = self.repository.get_by_studio(studio_uuid)
        return [AnimeResponse.model_validate(sa) for sa in studio_animes]

    def get_anime_by_uuid(self, anime_uuid:str):
        anime = self.repository.get_by_uuid(anime_uuid)
        return AnimeResponse.model_validate(anime)
