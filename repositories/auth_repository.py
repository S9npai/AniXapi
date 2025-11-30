from typing import Any, Dict, Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.refresh_token_model import RefreshToken
from models.user_model import User
import logging

logger = logging.getLogger(__name__)


class AuthRepository:
    def __init__(self, db:Session):
        self.db = db


    def add(self, user_data) -> User:
        try:
            new_user = User(**user_data)
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error adding new user: {e}", exc_info=True)
            raise


    def update(self, user:User, update_data:Dict[str, Any]):
        try:
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            self.db.commit()
            self.db.refresh(user)
            return user

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Can't update user data !: {e}", exc_info=True)
            raise


    def get_by_uuid(self, user_uuid) -> Optional[User]:
        try:
            return self.db.execute(select(User).where(
                User.uuid == user_uuid)
            ).scalar_one_or_none()

        except SQLAlchemyError as e:
            logger.error(f"Error fetching user by UUID: {e}", exc_info=True)
            raise


    def get_by_username(self, username:str) -> Optional[User]:
        try:
            return self.db.execute(select(User).where(
                User.username == username)
            ).scalar_one_or_none()

        except SQLAlchemyError as e:
            logger.error(f"Error fetching user by username: {e}", exc_info=True)
            raise


    def get_by_email(self, email:str) -> Optional[User]:
        try:
            return self.db.execute(select(User).where(
                User.email == email)
            ).scalar_one_or_none()

        except SQLAlchemyError as e:
            logger.error(f"Error fetching user by email: {e}", exc_info=True)
            raise


    def delete(self, user_uuid: str) -> bool:
        try:
            user_to_del = self.get_by_uuid(user_uuid)
            if not user_to_del:
                return False

            self.db.delete(user_to_del)
            self.db.commit()
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Can't delete user data !: {e}", exc_info=True)
            raise


    def add_refresh_token(self, token_data: Dict[str, Any]):
        try:
            new_token = RefreshToken(**token_data)
            self.db.add(new_token)
            self.db.commit()
            self.db.refresh(new_token)
            return new_token

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error adding new refresh token: {e}", exc_info=True)
            raise


    def get_refresh_token_jti(self, jti: str) -> Optional[RefreshToken]:
        try:
            return self.db.execute(select(RefreshToken).where(
                RefreshToken.id == jti)
            ).scalar_one_or_none()

        except SQLAlchemyError as e:
            logger.error(f"Error fetching refresh token by JTI: {e}", exc_info=True)
            raise


    def revoke_refresh_token(self, token: RefreshToken):
        try:
            token.is_revoked = True
            self.db.commit()
            self.db.refresh(token)
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Can't revoke refresh token !: {e}", exc_info=True)
            raise

