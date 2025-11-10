import logging
from typing import List
from uuid import uuid4
from utils.custom_exceptions import AlreadyExistsError, NotFoundError
from sqlalchemy.exc import IntegrityError
from repositories.anime_repository import AnimeRepository
from repositories.studio_repository import StudioRepository
from schemas.anime_validator import NewAnime, AnimeResponse, AnimeUpdate

logger = logging.getLogger(__name__)


class AnimeService:
    def __init__(self, anime_repo: AnimeRepository, studio_repo: StudioRepository):
        self.anime_repo = anime_repo
        self.studio_repo = studio_repo


    def add_new_anime(self, anime_data:NewAnime) -> AnimeResponse:
        studio = self.studio_repo.get_by_uuid(anime_data.studio_uuid)

        anime_dict = anime_data.model_dump()
        anime_dict["uuid"] = str(uuid4())
        anime_dict["studio"] = studio.uuid
        anime_dict.pop("studio_uuid", None)

        if not studio:
            raise NotFoundError(f"Studio doesn't exist")

        try:
            new_anime = self.anime_repo.add(anime_dict)
            logger.info(f"Created anime: {new_anime.name} (UUID: {new_anime.uuid})")
            return AnimeResponse.model_validate(new_anime)

        except IntegrityError as e:
            logger.error(f"Failed to create anime due to integrity error: {e}")
            raise AlreadyExistsError(f"Anime '{anime_data.name}' already exists")


    def get_all_anime(self) -> List[AnimeResponse]:
        animes = self.anime_repo.get_all()
        return [AnimeResponse.model_validate(a) for a in animes]


    def get_anime_by_name(self, anime_name:str):
        anime = self.anime_repo.get_by_name(anime_name)
        if not anime:
            raise NotFoundError(f"Anime named {anime_name} not found")
        return AnimeResponse.model_validate(anime)


    def get_anime_by_studio(self, studio_name:str):
        studio_animes = self.anime_repo.get_by_studio(studio_name)
        return [AnimeResponse.model_validate(sa) for sa in studio_animes]


    def get_anime_by_uuid(self, anime_uuid:str):
        anime = self.anime_repo.get_by_uuid(anime_uuid)
        if not anime:
            raise NotFoundError(f"Anime with UUID {anime_uuid} not found")
        return AnimeResponse.model_validate(anime)


    def update_anime(self, anime_uuid:str, anime_update:AnimeUpdate) -> AnimeResponse:
        existing_anime = self.anime_repo.get_by_name(anime_uuid)
        if not existing_anime:
            raise NotFoundError(f"Anime with UUID '{anime_uuid}' not found.")

        update_data = anime_update.model_dump(exclude_unset=True)

        if "studio_uuid" in update_data:
            studio_uuid = update_data.pop("studio_uuid")
            studio = self.studio_repo.get_by_uuid(studio_uuid)
            update_data["studio"] = studio.uuid

        try:
            updated_anime = self.anime_repo.update(existing_anime, update_data)
            logger.info(f"Updated anime: {updated_anime.name} (UUID: {anime_uuid})")
            return AnimeResponse.model_validate(updated_anime)

        except IntegrityError as e:
            logger.error(f"Failed to update anime due to integrity error: {e}")
            raise AlreadyExistsError(f"Cannot update: anime name already exists")


    def delete_anime(self, anime_uuid:str) -> bool:
        result = self.anime_repo.delete(anime_uuid)
        if result:
            logger.info(f"Deleted anime with UUID: {anime_uuid}")
        return result

