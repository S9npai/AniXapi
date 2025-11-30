import uuid
from datetime import datetime, timedelta, timezone
import jwt
from settings import settings
from jwt import ExpiredSignatureError, InvalidTokenError
from utils.custom_exceptions import NotFoundError, ValidityError
from pydantic import UUID


def create_access_token(data: dict, expire_delta: timedelta | None = None) -> str:
    jwt_token = data.copy()
    if "sub" not in jwt_token:
        raise ValueError("Token payload must contain a 'sub' claim")

    jwt_token["type"] = "access"

    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    jwt_token.update({"exp": expire})

    encoded_jwt = jwt.encode(jwt_token, settings.jwt_secret, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(data: dict, expire_delta: timedelta | None = None) -> str:
    jwt_token = data.copy()
    if "sub" not in jwt_token:
        raise ValueError("Token payload must contain a 'sub' claim")

    jwt_token["type"] = "refresh"

    jti = (uuid.uuid4())
    jwt_token["jti"] = jti

    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.refresh_token_expire_minutes)
    jwt_token.update({"exp": expire})

    encoded_jwt = jwt.encode(jwt_token, settings.jwt_secret, algorithm=settings.algorithm)
    return encoded_jwt


def verify_jwt(token: str, expected_type: str = "access") -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithm=settings.algorithm)
        user_uuid: str = payload.get("sub")
        token_type: str = payload.get("type")

        if user_uuid is None:
            raise NotFoundError(f"User wih UUID {user_uuid} not found")

        if token_type != expected_type:
            raise ValidityError(f"Invalid token type. Expected {expected_type}, got {token_type}")

        return payload

    except ExpiredSignatureError:
        raise ValidityError("Token has expired !")

    except InvalidTokenError:
        raise ValidityError(f"Invalid token")

