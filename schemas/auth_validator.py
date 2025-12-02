from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator


class UserRegister(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=4, max_length=20)
    password: Optional[str] = Field(None, min_length=8, max_length=64)
    email: Optional[EmailStr] = Field(None)


class UserLogin(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str

    @model_validator(mode='after')
    def check_one_identifier(self):
        if not (self.username or self.email):
            raise ValueError("You must provide either a username or an email to log in")
        return self


class UserResponse(BaseModel):
    uuid: str
    username: str
    email: EmailStr
    role: Literal["user", "admin"]
    created_at: datetime

    model_config = ConfigDict(from_attributes = True)


class ResetPassword(BaseModel):
    token: str


class ForgotPassword(BaseModel):
    email: EmailStr


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RefreshToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

