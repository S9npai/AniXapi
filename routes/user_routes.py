from fastapi import APIRouter, FastAPI, Depends
from controllers.auth_controller import *
from schemas.auth_validator import *
from utils.db_connection import *
from middleware.Auth import *

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)


