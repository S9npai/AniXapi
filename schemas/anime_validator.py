from datetime import date
from typing import Literal, Optional, List
from pydantic import BaseModel, PositiveInt, ConfigDict, model_validator, UUID4
from schemas.studio_validator import StudioResponse


class NewAnime(BaseModel):
    name: str
    jp_name: str
    episodes: PositiveInt
    format: Literal["TV", "movie", "OVA", "ONA"]
    start_date: date
    end_date: date
    studio_uuids: List[UUID4]

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after')
    def check_anime_dates(self):
        if self.start_date > self.end_date:
            raise ValueError("start date can't come after end date !")
        return self


class AnimeResponse(BaseModel):
    uuid: UUID4
    name: str
    jp_name: str
    episodes: PositiveInt
    format: Literal["TV", "movie", "OVA", "ONA"]
    start_date: date
    end_date: date
    studios: List[StudioResponse]

    model_config = ConfigDict(from_attributes=True)

    """@field_serializer('uuid')
    def serialize_uuid(self, uuid_binary:bytes) -> str:
        return binary_to_uuid(uuid_binary)"""
    # no longer needed after the SQLAlchemy custom type


class AnimeUpdate(BaseModel):
    name: Optional[str] = None
    jp_name: Optional[str] = None
    episodes: Optional[PositiveInt] = None
    format: Optional[Literal["TV", "movie", "OVA", "ONA"]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    studio_uuids: Optional[List[UUID4]] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after')
    def check_anime_dates(self):
        if self.start_date is not None and self.end_date is not None:
            if self.start_date > self.end_date:
                raise ValueError("start date can't come after end date !")
        return self

