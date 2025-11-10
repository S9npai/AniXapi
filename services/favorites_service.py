from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from repositories.favorites_repository import FavoritesRepository
from schemas.favorites_validator import FavoritesValidator

class FavoritesService:
    def __init__(self, repository:FavoritesRepository):
        self.repository = repository

    def add_new_favorite(self, fav_data:FavoritesValidator):
        fav_dict = fav_data.model_dump()
        try:
            new_fav = self.repository.add(fav_dict)
            return FavoritesValidator.model_validate(new_fav)
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Favorite record already exists or constraint violation")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def delete_favorite(self, user:UUID4, anime_name:str):
        self.repository.delete(user ,anime_name)

    def get_all_favorites(self):
        favorites = self.repository.get_all()
        return [FavoritesValidator.model_validate(f) for f in favorites]

