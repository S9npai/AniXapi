from typing import List
from fastapi import APIRouter
from controllers.studio_controller import add_new_studio, update_studio, get_all_studios, delete_studio
from schemas.studio_validator import StudioResponse, StudioValidator, StudioUpdate

router = APIRouter(
    tags=["Studio"],
    prefix="/studios"
)


@router.post("/", response_model=StudioResponse)
def create_studio(studio_data: StudioValidator):
    return add_new_studio(studio_data)

@router.get("/all", response_model=List[StudioResponse])
def fetch_all_studios():
    return get_all_studios()

@router.delete("/", response_model=StudioResponse)
def del_studio(studio:StudioResponse):
    return delete_studio(studio)

@router.patch("/", response_model=StudioResponse)
def update_studio_data(studio_data:StudioResponse, studio_new_data:StudioUpdate):
    return update_studio(studio_data, studio_new_data)


