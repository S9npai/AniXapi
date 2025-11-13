from services.auth_service import AuthService, get_current_user
from sqlalchemy.orm import Session
from models.user_model import User
from fastapi import Depends
from repositories.auth_repository import AuthRepository
from schemas.auth_validator import UserResponse, UserRegister, UserLogin
from services.auth_service import AuthService
from utils.db_connection import db_conn


def get_auth_service(db:Session = Depends(db_conn)) -> AuthService:
    repo = AuthRepository(db)
    return AuthService(repo)


def get_running_user(user:UserResponse = Depends(get_current_user)) -> UserResponse:
    return user


def user_register(user_data:UserRegister, service:AuthService = Depends(get_auth_service)):
    return service.register_user(user_data)


def user_login(user_data:UserLogin , service:AuthService = Depends(get_auth_service)):
    return service.login_user(user_data)


