import argon2, jwt, os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from argon2 import PasswordHasher
from argon2.exceptions import *
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Literal
from schemas.auth_validator import UserResponse
from utils.db_connection import db_conn

load_dotenv()
ph = PasswordHasher()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def fetch_current_user_payload(token: str = Depends(oauth2_scheme)) -> dict:
    payload = verify_jwt(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-authenticate": "bearer"},
        )

    return payload


def get_current_user(
    payload: dict = Depends(fetch_current_user_payload), db: Session = Depends(db_conn)) -> UserResponse:
    user_uuid = payload.get("sub")


def verify_password(plain_password, hashed_password) -> tuple[bool, str | None]:
    try:
        match = ph.verify(hashed_password, plain_password)

        if match and ph.check_needs_rehash(hashed_password):
            return True, ph.hash(plain_password)

        return True, None

    except (InvalidHashError, VerifyMismatchError):
        return False, None


def create_access_token(data: dict, expire_delta: timedelta | None = None) -> str:
    wt_load = data.copy()
    if "sub" not in wt_load:
        raise ValueError("Token payload must contain a 'sub' claim")

    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    wt_load.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(wt_load, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not create access token")


def verify_jwt(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
        user_id: str = payload.get("sub")

        if user_id is None:
            return None

        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class RoleChecker:
    def __init__(self, required_role: Literal["user", "admin"]):
        self.required_role = required_role

    def __call__(self, payload: dict = Depends(fetch_current_user_payload)):
        user_role = payload.get("role")

        if user_role != self.required_role:
            raise HTTPException(
                status_code=403,
                detail=f"Unauthorized. Requires role: '{self.required_role}'",
            )

        return True


