import logging
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

logger = logging.getLogger(__name__)
ph = PasswordHasher()


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
