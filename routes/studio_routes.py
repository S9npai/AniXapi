from typing import List
from fastapi import APIRouter
from controllers.studio_controller import add_new_studio, update_studio, get_all_studios, delete_studio, get_studio_name
from schemas.studio_validator import StudioResponse, StudioValidator, StudioUpdate

router = APIRouter(
    tags=["Studio"],
    prefix="/studios"
)


router.post("/", response_model=StudioResponse)(add_new_studio)

router.get("/all", response_model=List[StudioResponse])(get_all_studios)

router.delete("/", response_model=StudioResponse)(delete_studio)

router.patch("/", response_model=StudioResponse)(update_studio)

router.get("/{studio_name}", response_model=StudioResponse)(get_studio_name)

