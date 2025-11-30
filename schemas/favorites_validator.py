from pydantic import BaseModel, UUID4, ConfigDict


class FavoritesValidator(BaseModel):
    user: UUID4
    anime: UUID4

    model_config = ConfigDict(from_attributes=True)

