import logging
from typing import List
from uuid import uuid4
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from repositories.studio_repository import StudioRepository
from schemas.studio_validator import StudioResponse, StudioValidator, StudioUpdate
from utils.custom_exceptions import NotFoundError, AlreadyExistsError

logger = logging.getLogger(__name__)


class StudioService:
    def __init__(self, repo:StudioRepository):
        self.repo = repo


    def add_studio(self, studio_data:StudioValidator):
        studio_dict = studio_data.model_dump()
        studio_dict["uuid"] = str(uuid4())

        try:
            new_studio = self.repo.add(studio_dict)
            return StudioResponse.model_validate(new_studio)

        except IntegrityError as e:
            raise AlreadyExistsError(f"Studio with the same data already exists !: {str(e)}")


    def get_all_studios(self) -> List[StudioResponse]:
        studios = self.repo.get_all()
        return [StudioResponse.model_validate(s) for s in studios]


    def get_studio_by_name(self, studio_name:str):
        studio = self.repo.get_by_name(studio_name)
        if not studio:
            raise NotFoundError(f"Studio named {studio_name} not found")
        return StudioResponse.model_validate(studio)


    def get_studio_by_uuid(self, studio_uuid:str):
        studio = self.repo.get_by_uuid(studio_uuid)
        if not studio:
            raise NotFoundError(f"Studio with UUID '{studio_uuid}' not found.")
        return StudioResponse.model_validate(studio)


    def update_studio(self, studio_uuid:str, studio_update:StudioUpdate):
        existing_studio = self.repo.get_by_uuid(studio_uuid)
        if not existing_studio:
            raise NotFoundError(f"Studio with UUID '{studio_uuid}' not found.")

        update_data = studio_update.model_dump(exclude_unset=True)

        try:
            updated_studio = self.repo.update(existing_studio, update_data)
            logger.info(f"Updated studio: {updated_studio.name} (UUID: {studio_uuid})")
            return StudioResponse.model_validate(updated_studio)

        except IntegrityError as e:
            logger.error(f"Failed to update studio due to integrity error: {e}")
            raise AlreadyExistsError(f"Studio already exists")


    def delete_studio(self, studio_uuid: str) -> bool:
        result = self.repo.delete(studio_uuid)
        if result:
            logger.info(f"Deleted studio with UUID: {studio_uuid}")
        return result

