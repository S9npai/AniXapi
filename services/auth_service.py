import logging
import uuid
from datetime import datetime, timezone
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from middleware.Auth import get_payload
from repositories.auth_repository import AuthRepository
from schemas.auth_validator import UserResponse, UserRegister, UserLogin, TokenPair
from utils.custom_exceptions import UnauthorizedError, AlreadyExistsError, ValidityError, NotFoundError
from utils.db_connection import db_conn
from utils.jwt_utils import create_access_token, create_refresh_token, verify_jwt
from utils.password_utils import hash_password, verify_and_rehash_password

logger = logging.getLogger(__name__)


def get_current_user(payload: dict = Depends(get_payload), db: Session = Depends(db_conn)) -> UserResponse:
    user_uuid = payload.get("sub")

    if user_uuid is None:
        raise NotFoundError(f"Invalid token payload, didn't find user ID")

    auth_repo = AuthRepository(db)
    user = auth_repo.get_by_uuid(user_uuid)

    if not user:
        raise UnauthorizedError("Unauthorized !")
    return UserResponse.model_validate(user)


class AuthService:
    def __init__(self, repo:AuthRepository):
        self.repo = repo

    def register_user(self, user_data:UserRegister):
        existing_user_email = self.repo.get_by_email(user_data.email)
        existing_user_username = self.repo.get_by_username(user_data.username)

        if existing_user_username or existing_user_email:
            raise AlreadyExistsError("This user already exists !")

        hashed_password = hash_password(user_data.password)

        user_dict = user_data.model_dump()
        user_dict["uuid"] = str(uuid.uuid4())
        user_dict["password_hash"] = hashed_password
        user_dict.pop("password")

        try:
            new_user = self.repo.add(user_dict)
            return UserResponse.model_validate(new_user)

        except IntegrityError as e:
            logger.error(f"Failed to register user, integrity error")
            raise AlreadyExistsError(f"User already exists: {e}")


    def login_user(self, user_data:UserLogin):
        user = None

        if user_data.username:
            user = self.repo.get_by_username(user_data.username)
        elif user_data.email:
            user = self.repo.get_by_email(user_data.email)

        if not user:
            raise UnauthorizedError("Incorrect credentials")

        is_verified, new_hash = verify_and_rehash_password(user_data.password, user.password_hash)

        if not is_verified:
            raise UnauthorizedError("Incorrect credentials")

        if new_hash:
            user.password_hash = new_hash
            self.repo.update(user, {"password_hash": new_hash})

        access_token = create_access_token(str(user.uuid), user.role)
        refresh_token, jti, expires_at = create_refresh_token(str(user.uuid))

        refresh_token_data = {
            "id": jti,
            "user_uuid": str(user.uuid),
            "expires_at": expires_at,
            "is_revoked": False
        }

        try:
            self.repo.add_refresh_token(refresh_token_data)
        except Exception as e:
            logger.error(f"Failed to store refresh token: {e}")
            raise

        return TokenPair(access_token=access_token, refresh_token=refresh_token)


    # implements token revocation & rotation for enhanced security
    def refresh_access_token(self, refresh_token: str):
        try:
            payload = verify_jwt(refresh_token, expected_type="refresh")
        except ValidityError as e:
            raise UnauthorizedError(f"Not a valid refresh token: {str(e)}")

        jti = payload.get("jti")
        user_uuid = payload.get("sub")

        if not user_uuid or not jti:
            raise UnauthorizedError(f"Invalid refresh token payload")

        stored_token = self.repo.get_refresh_token_jti(jti)

        if not stored_token:
            raise UnauthorizedError("Refresh token not found")

        if stored_token.is_revoked:
            logger.warning(f"Revoking, token reuse detected for user {user_uuid}")
            self.repo.revoke_user_tokens(user_uuid)
            raise UnauthorizedError("Token has been revoked")

        if stored_token.expires_at < datetime.now(timezone.utc):
            raise UnauthorizedError(f"Refresh token has expired")

        user = self.repo.get_by_uuid(user_uuid)

        if not user:
            raise NotFoundError("User no longer exists !")

        self.repo.revoke_refresh_token(stored_token)

        access_token = create_access_token(str(user.uuid), user.role)
        new_refresh_token, new_jti, expires_at = create_refresh_token(str(user.uuid))

        new_refresh_token_data = {
            "id": new_jti,
            "user_uuid": str(user.uuid),
            "expires_at": expires_at,
            "is_revoked": False,
        }

        try:
            self.repo.add_refresh_token(new_refresh_token_data)
        except Exception as e:
            logger.error(f"Failed to store new refresh token: {e}")
            raise

        return TokenPair(access_token=access_token, refresh_token=new_refresh_token)


    def logout(self, refresh_token: str):
        try:
            payload = verify_jwt(refresh_token, "refresh")
        except:
            raise UnauthorizedError(f"Invalid refresh token")

        jti = payload.get("jti")
        if not jti:
            raise UnauthorizedError(f"Not a valid JWT token payload")

        stored_token = self.repo.get_refresh_token_jti(jti)
        if not stored_token:
            raise NotFoundError(f"Refresh token not found !")

        self.repo.revoke_refresh_token(stored_token)
        return {"message": "logged out successfully !"}


    def logout_all_devices(self, user_uuid):
        user = self.repo.get_by_uuid(user_uuid)

        if not user:
            raise NotFoundError(f"User with UUID {user_uuid} doesn't exist !")

        count = self.repo.revoke_user_tokens(user_uuid)
        return {"message": f"Logged out successfully out of {count} devices"}

