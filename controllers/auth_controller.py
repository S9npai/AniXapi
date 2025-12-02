from fastapi import Depends, Body
from sqlalchemy.orm import Session
from repositories.auth_repository import AuthRepository
from schemas.auth_validator import UserResponse, UserRegister, UserLogin
from services.auth_service import AuthService, get_current_user
from utils.db_connection import db_conn


def get_auth_service(db:Session = Depends(db_conn)) -> AuthService:
    repo = AuthRepository(db)
    return AuthService(repo)


def get_running_user(user:UserResponse = Depends(get_current_user)) -> UserResponse:
    return user


def user_register(user_data:UserRegister, service:AuthService = Depends(get_auth_service)):
    return service.register_user(user_data)


def user_login(user_data:UserLogin, service:AuthService = Depends(get_auth_service)):
    return service.login_user(user_data)


def refresh_tokens(refresh_token: str = Body(..., embed=True), service:AuthService = Depends(get_auth_service)):
    return service.refresh_access_token(refresh_token)


def logout(refresh_token: str = Body(..., embed=True), service:AuthService = Depends(get_auth_service)):
    return service.logout(refresh_token)


def logout_all(user: UserResponse = Depends(get_running_user) , service:AuthService = Depends(get_auth_service)):
    return service.logout_all_devices(user.uuid)

