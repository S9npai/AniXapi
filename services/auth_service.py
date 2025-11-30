import logging
import uuid
from sqlalchemy.exc import IntegrityError
from repositories.auth_repository import AuthRepository
from schemas.auth_validator import UserResponse, UserRegister, UserLogin, AccessToken
from utils.custom_exceptions import UnauthorizedError, AlreadyExistsError
from utils.jwt_utils import create_access_token
from utils.password_utils import hash_password, verify_and_rehash_password

logger = logging.getLogger(__name__)


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

        data = {"sub": str(user.uuid), "role": user.role}
        access_token = create_access_token(data=data)

        return AccessToken(access_token=access_token)


