import uuid
from uuid import uuid4
from typing import List
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from repositories.studio_repository import StudioRepository
from schemas.studio_validator import StudioResponse, StudioValidator, StudioUpdate


class StudioService:
    def __init__(self, repository:StudioRepository):
        self.repository = repository

    def get_studio_uuid(self, studio_uuid:str):
        studio = self.repository.get_by_uuid(studio_uuid)
        return StudioResponse.model_validate(studio)

    def add_studio(self, studio_data:StudioValidator):
        studio_dict = studio_data.model_dump()
        studio_data["uuid"] = str(uuid4())

        try:
            new_anime = self.repository.add(studio_dict)
            return StudioResponse.model_validate(new_anime)

        except IntegrityError:
            raise HTTPException(status_code=400, detail="Integrity error !")

    def get_all_studios(self) -> List[StudioResponse]:
        studios = self.repository.get_all()
        return [StudioResponse.model_validate(a) for a in studios]

    def delete_studio(self, studio_uuid: str) -> bool:
        return self.repository.delete(studio_uuid)

    def get_studio_by_name(self, name:str):
        return self.repository.get_by_name(name)

    def update_studio(self, studio_uuid:str, studio_update:StudioUpdate):
        existing_studio = self.repository.get_by_uuid(studio_uuid)
        if not existing_studio:
            raise HTTPException(status_code=404, detail=f"Studio with UUID '{studio_uuid}' not found.")

        update_data = studio_update.model_dump()

        try:
            updated_studio = self.repository.update(existing_studio, update_data)

        except IntegrityError:
            raise HTTPException(status_code=400, detail="Database integrity error during studio update !")

