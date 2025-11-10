from fastapi import APIRouter, FastAPI, Depends
from controllers.auth_controller import *
from schemas.auth_validator import *
from utils.db_connection import *

router = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
)

router.post("/register")()

router.post("/login")()

router.get("/logout")()

