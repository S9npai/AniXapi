import pydantic, uuid
from pydantic import BaseModel, ConfigDict, field_serializer
from typing import Optional, Literal
from utils.uuid_conv import *

class StudioValidator(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

class StudioResponse(BaseModel):
    uuid: str
    name: str

    model_config = ConfigDict(from_attributes=True)

    """@field_serializer('uuid')
    def serialize_uuid(self, uuid_binary:bytes) -> str:
        return binary_to_uuid(uuid_binary)"""

class StudioUpdate(BaseModel):
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

