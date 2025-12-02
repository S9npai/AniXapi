from fastapi import APIRouter
from controllers.auth_controller import user_register, get_running_user, user_login, logout_all, logout, refresh_tokens
from schemas.auth_validator import UserResponse, AccessToken, TokenPair

router = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
)

router.post("/register", response_model=UserResponse)(user_register)

router.post("/login", response_model=TokenPair)(user_login)

router.get("/me", response_model=UserResponse)(get_running_user)

router.post("/refresh", response_model=TokenPair)(refresh_tokens)

router.post("/logout")(logout)

router.post("/logout-all")(logout_all)

