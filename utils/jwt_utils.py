import uuid
from datetime import datetime, timedelta, timezone
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from pydantic import UUID
import config
from project_settings import settings
from utils.custom_exceptions import NotFoundError, ValidityError

issuer = config.PROJECT_NAME


def create_access_token(user_uuid: str, role: str) -> str:
    issued_at = int(datetime.now(timezone.utc).timestamp())
    expire = int((datetime.now(timezone.utc) +
                  timedelta(minutes=settings.refresh_token_expire_minutes)).timestamp())
    sub = user_uuid


    jwt_token = {
        "iat": issued_at,
        "exp": expire,
        "sub": sub,
        "iss": issuer,
        "type": "access",
        "role": role
    }

    encoded_jwt = jwt.encode(jwt_token, settings.jwt_secret, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(user_uuid: str):
    issued_at = int(datetime.now(timezone.utc).timestamp())
    expire_dt = datetime.now(timezone.utc) + timedelta(minutes=settings.refresh_token_expire_minutes)
    expire = int(expire_dt.timestamp())
    sub = user_uuid
    jti = uuid.uuid4()


    jwt_token = {
        "iat": issued_at,
        "exp": expire,
        "sub": sub,
        "iss": issuer,
        "type": "refresh",
        "jti": str(jti)
    }

    encoded_jwt = jwt.encode(jwt_token, settings.jwt_secret, algorithm=settings.algorithm)
    return encoded_jwt, jti, expire_dt


def verify_jwt(token: str, expected_type: str) -> dict:
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

