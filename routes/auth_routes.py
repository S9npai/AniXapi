from fastapi import APIRouter
from controllers.auth_controller import user_register, get_running_user, user_login, logout_all
from schemas.auth_validator import UserResponse, AccessToken, TokenPair

router = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
)

router.post("/register", response_model=UserResponse)(user_register)

router.post("/login", response_model=TokenPair)(user_login)

router.get("/me", response_model=UserResponse)(get_running_user)

router.get("/logout-all")(logout_all)

