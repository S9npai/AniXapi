from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from repositories.favorites_repository import FavoritesRepository
from schemas.anime_validator import AnimeResponse
from schemas.favorites_validator import FavoritesValidator
from utils.custom_exceptions import AlreadyExistsError


class FavoritesService:
    def __init__(self, repository:FavoritesRepository):
        self.repository = repository

    def add_new_favorite(self, fav_data:FavoritesValidator):
        fav_dict = fav_data.model_dump()
        try:
            new_fav = self.repository.add(fav_dict)
            return FavoritesValidator.model_validate(new_fav)
        except SQLAlchemyError as e:
            raise AlreadyExistsError(f"Favorite record already exists !: {e}")

    def delete_favorite(self, user_uuid:str, anime_uuid:str):
        return self.repository.delete(user_uuid ,anime_uuid)

    def get_user_favs(self, user_uuid:str):
        favorites = self.repository.get_user_favorites(user_uuid)
        return [AnimeResponse.model_validate(f) for f in favorites]
