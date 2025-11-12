from typing import List
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from services.auth_service import verify_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_payload(token: str = Depends(oauth2_scheme)) -> dict:
    payload = verify_jwt(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "bearer"},
        )
    return payload


class RoleChecker:
    def __init__(self, roles: List[str]):
        self.roles = roles

    def __call__(self, payload: dict = Depends(get_payload)):
        user_role = payload.get("role")

        if not user_role:
            raise HTTPException(status_code=401, detail="No specified role in token")

        if user_role not in self.roles:
            raise HTTPException(
                status_code=403,
                detail=f"Invalid role, requires either {', '.join(self.roles)}"
            )
        return payload

