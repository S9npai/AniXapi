import pydantic
from pydantic import BaseModel, NonNegativeFloat, Field, field_serializer
from utils.uuid_conv import binary_to_uuid


class RatingValidator(BaseModel):
    anime: str
    user: str
    value: NonNegativeFloat = Field(ge=0, le=5)

    @field_serializer('anime')
    def serialize_anime_uuid(self, uuid_binary:bytes) -> str:
        return binary_to_uuid(uuid_binary)

    @field_serializer('user')
    def serialize_user_uuid(self, uuid_binary:bytes) -> str:
        return binary_to_uuid(uuid_binary)

