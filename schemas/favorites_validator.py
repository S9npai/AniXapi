from pydantic import BaseModel, UUID4

class FavoritesValidator(BaseModel):
    user: UUID4
    anime: UUID4

