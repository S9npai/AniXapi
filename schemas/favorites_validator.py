import pydantic
from pydantic import field_serializer, BaseModel, UUID4

from utils.uuid_conv import binary_to_uuid


class FavoritesValidator(BaseModel):
    user_uuid: UUID4
    anime_uuid: UUID4

    @field_serializer('user_uuid')
    def serialize_user_uuid(self, uuid_binary:bytes) -> str:
        return binary_to_uuid(uuid_binary)

    @field_serializer('anime_uuid')
    def serialize_anime_uuid(self, uuid_binary:bytes) -> str:
        return binary_to_uuid(uuid_binary)

