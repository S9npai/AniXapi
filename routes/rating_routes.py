from fastapi import APIRouter, FastAPI, Depends
from controllers.rating_controller import *
from schemas.rating_validator import *
from utils.db_connection import *

router = APIRouter(
    tags=["Rating"],
    prefix="/rating"
)

router.post()

