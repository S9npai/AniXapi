import logging
import uuid

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from middleware.Auth import get_payload
from repositories.auth_repository import AuthRepository
from schemas.auth_validator import UserResponse, UserRegister
from utils.custom_exceptions import NotFoundError, UnauthorizedError, AlreadyExistsError
from utils.db_connection import db_conn

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, repo:AuthRepository):
        self.repo = repo

    def get_current_user(self, payload: dict = Depends(get_payload), db: Session = Depends(db_conn)) -> UserResponse:
        user_uuid = payload.get("sub")

        if user_uuid is None:
            raise NotFoundError(f"Invalid token payload, didn't find user ID")

        auth_repo = AuthRepository(db)
        user = auth_repo.get_by_uuid(user_uuid)

        if not user:
            raise UnauthorizedError("Unauthorized !")
        return UserResponse.model_validate(user)


    def register_user(self, user_data:UserRegister):
        user_dict = user_data.model_dump()
        user_dict["uuid"] = str(uuid.uuid4)

        try:
            new_user = self.repo.add(user_dict)
            return UserResponse.model_validate(new_user)

        except IntegrityError as e:
            raise AlreadyExistsError(f"User already exists: {e}")


    def login_user(self):


