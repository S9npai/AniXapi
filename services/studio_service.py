from uuid import uuid4
from typing import List
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from repositories.studio_repository import StudioRepository
from schemas.studio_validator import StudioResponse, StudioValidator, StudioUpdate


class StudioService:
    def __init__(self, repository:StudioRepository):
        self.repository = repository

    def get_studio_by_uuid(self, studio_uuid:str):
        studio = self.repository.get_by_uuid(studio_uuid)
        if not studio:
            raise HTTPException(status_code=404, detail=f"Studio with UUID '{studio_uuid}' not found.")
        return StudioResponse.model_validate(studio)

    def add_studio(self, studio_data:StudioValidator):
        studio_dict = studio_data.model_dump()
        studio_dict["uuid"] = str(uuid4())

        try:
            new_studio = self.repository.add(studio_dict)
            return StudioResponse.model_validate(new_studio)
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Studio name already exists or constraint violation")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def get_all_studios(self) -> List[StudioResponse]:
        studios = self.repository.get_all()
        return [StudioResponse.model_validate(s) for s in studios]

    def delete_studio(self, studio_uuid: str) -> bool:
        return self.repository.delete(studio_uuid)

    def get_studio_by_name(self, name:str):
        return self.repository.get_by_name(name)

    def update_studio(self, studio_uuid:str, studio_update:StudioUpdate):
        existing_studio = self.repository.get_by_uuid(studio_uuid)
        if not existing_studio:
            raise HTTPException(status_code=404, detail=f"Studio with UUID '{studio_uuid}' not found.")

        update_data = studio_update.model_dump(exclude_unset=True)

        try:
            updated_studio = self.repository.update(existing_studio, update_data)
            return StudioResponse.model_validate(updated_studio)
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Studio name already exists or constraint violation")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
