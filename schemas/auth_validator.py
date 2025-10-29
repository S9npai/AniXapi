import pydantic, re
from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator, field_serializer
from typing import Optional, Literal
from datetime import datetime
from utils.uuid_conv import *

class UserCreate(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


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
    email: str
    role: Literal["user", "admin"]
    created_at: datetime

    model_config = ConfigDict(from_attributes = True)

    @field_serializer('uuid')
    def serialize_uuid(self, uuid_binary:bytes) -> str:
        return binary_to_uuid(uuid_binary)


class ResetPassword(BaseModel):
    token: str
    email: EmailStr


class ForgotPassword(BaseModel):
    email: EmailStr


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"

