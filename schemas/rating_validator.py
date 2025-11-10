from pydantic import BaseModel, NonNegativeFloat, Field


class RatingValidator(BaseModel):
    anime: str
    user: str
    value: NonNegativeFloat = Field(ge=0, le=5)


