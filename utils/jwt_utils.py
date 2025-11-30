from datetime import datetime, timedelta, timezone
import jwt
from settings import settings
from jwt import ExpiredSignatureError, InvalidTokenError
from utils.custom_exceptions import NotFoundError, ValidityError


def create_access_token(data: dict, expire_delta: timedelta | None = None) -> str:
    jwt_token = data.copy()
    if "sub" not in jwt_token:
        raise ValueError("Token payload must contain a 'sub' claim")

    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    jwt_token.update({"exp": expire})

    encoded_jwt = jwt.encode(jwt_token, settings.jwt_secret, algorithm=settings.algorithm)
    return encoded_jwt


def verify_jwt(token:str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithm=settings.algorithm)
        user_uuid: str = payload.get("sub")

        if user_uuid is None:
            raise NotFoundError(f"User wih UUID {user_uuid} not found")
        return payload

    except ExpiredSignatureError:
        raise ValidityError("Token has expired !")

    except InvalidTokenError:
        raise ValidityError(f"Invalid token")

