from pydantic import ConfigDict, BaseModel, Field


class RatingCreate(BaseModel):
    anime_uuid: str
    value: float = Field(ge=0, le=5)


class RatingResponse(BaseModel):
    anime_uuid: str
    user_uuid: str
    value: float

    model_config = ConfigDict(from_attributes=True)

