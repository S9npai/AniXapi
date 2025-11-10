import jwt, os
from datetime import timezone, datetime, timedelta
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from dotenv import load_dotenv
from fastapi import Depends
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session
from middleware.Auth import get_payload
from repositories.auth_repository import AuthRepository
from utils.custom_exceptions import NotFoundError
from utils.db_connection import db_conn
import logging

logger = logging.getLogger(__name__)

load_dotenv()
ph = PasswordHasher()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def hash_password(plain_password):
    hashed = ph.hash(plain_password)
    return hashed


def verify_and_rehash_password(plain_password, hashed_password) -> tuple[bool, str | None]:
    try:
        match = ph.verify(hashed_password, plain_password)

        if match and ph.check_needs_rehash(hashed_password):
            return True, ph.hash(plain_password)
        return True, None

    except (InvalidHashError, VerifyMismatchError) as e:
        logger.warning(f"Password verification failed: {e}")
        return False, None


def create_access_token(data: dict, expire_delta: timedelta | None = None) -> str:
    jwt_token = data.copy()
    if "sub" not in jwt_token:
        raise ValueError("Token payload must contain a 'sub' claim")

    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_token.update({"exp": expire})

    encoded_jwt = jwt.encode(jwt_token, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_jwt(token:str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
        user_uuid: str = payload.get("sub")

        if user_uuid is None:
            raise NotFoundError(f"User wih UUID {user_uuid} not found")
        return payload

    except ExpiredSignatureError:
        raise "Token has expired !"

    except InvalidTokenError:
        raise f"Invalid token"


def get_current_user(payload: dict = Depends(get_payload), db: Session = Depends(db_conn)):
    user_uuid = payload.get("sub")

    if user_uuid is None:
        raise NotFoundError(f"Invalid token payload, didn't find user ID")

    auth_repo = AuthRepository(db)
    user = auth_repo.get_by_uuid(user_uuid)

    if not user:
        raise NotFoundError("User not found")
    return user
