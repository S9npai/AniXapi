from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from middleware.auth import verify_password, create_access_token
from models import user_model
from models.user_model import User
from schemas.auth_validator import UserResponse, UserCreate, UserLogin, AccessToken
from utils.uuid_conv import uuid_to_binary, binary_to_uuid
from argon2 import PasswordHasher

ph = PasswordHasher()


def register_user(user:UserCreate, db:Session) -> UserResponse:
    try:
        existing_user = db.execute(
            select(User).where(
                (User.email == user.email) |
                (User.username == user.username)
            )
        ).scalar_one_or_none()

        if existing_user:
            if existing_user.email == str(user.email).lower():
                raise HTTPException(
                    status_code=400,
                    detail="A user with this email already exists"
                )
            elif existing_user.username == user.username:
                raise HTTPException(
                    status_code=400,
                    detail="Username already used by someone else !"
                )

        hashed_password = ph.hash(user.password)

        new_user = user_model.User(
            uuid=uuid4().bytes,
            username=user.username,
            email=str(user.email).lower(),
            password=hashed_password,
            role="user"
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Bad request"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error :{e}"
        )

    return UserResponse.model_validate(new_user)


def user_login(user_creds: UserLogin, db:Session) -> AccessToken:
    conditions = []

    if user_creds.username:
        conditions.append(User.username == user_creds.username)

    if user_creds.email:
        conditions.append(User.email == str(user_creds.email).lower())

    user = db.execute(
        select(User).where(or_(*conditions))
    ).scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    password_match, new_hash = verify_password(user_creds.password, user.password)

    if not password_match:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if new_hash:
        user.password = new_hash
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(
        data={
            "sub": binary_to_uuid(user.uuid),
            "role": user.role,
        }
    )

    return AccessToken.model_validate({"access_token": access_token, "token_type":"bearer"})


def get_user_by_username(username:str, db:Session) -> UserResponse:
    user = db.execute(
        select(User).where(User.username == username)
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found !"
        )

    return UserResponse.model_validate(user)


def get_user_by_uuid(user_uuid:str, db:Session) -> UserResponse:
    binary_uuid = uuid_to_binary(user_uuid)

    user = db.execute(
        select(User).where(User.uuid == binary_uuid)
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found !"
        )

    return UserResponse.model_validate(user)

