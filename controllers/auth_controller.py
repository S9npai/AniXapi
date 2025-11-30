from fastapi import Depends
from sqlalchemy.orm import Session
from middleware.Auth import get_payload
from repositories.auth_repository import AuthRepository
from schemas.auth_validator import UserResponse, UserRegister, UserLogin
from services.auth_service import AuthService
from utils.custom_exceptions import NotFoundError, UnauthorizedError
from utils.db_connection import db_conn


def get_current_user(payload: dict = Depends(get_payload), db: Session = Depends(db_conn)) -> UserResponse:
    user_uuid = payload.get("sub")

    if user_uuid is None:
        raise NotFoundError(f"Invalid token payload, didn't find user ID")

    auth_repo = AuthRepository(db)
    user = auth_repo.get_by_uuid(user_uuid)

    if not user:
        raise UnauthorizedError("Unauthorized !")
    return UserResponse.model_validate(user)


def get_auth_service(db:Session = Depends(db_conn)) -> AuthService:
    repo = AuthRepository(db)
    return AuthService(repo)


def get_running_user(user:UserResponse = Depends(get_current_user)) -> UserResponse:
    return user


def user_register(user_data:UserRegister, service:AuthService = Depends(get_auth_service)):
    return service.register_user(user_data)


def user_login(user_data:UserLogin , service:AuthService = Depends(get_auth_service)):
    return service.login_user(user_data)


