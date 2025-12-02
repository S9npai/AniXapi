import logging
from models.rating_model import Rating
from repositories.rating_repository import RatingRepository

logger = logging.getLogger(__name__)


class RatingService:
    def __init__(self, repo:RatingRepository):
        self.repo = repo


    def set_rating(self, user_uuid: str, anime_uuid: str, value: float) -> bool:
        existing_rating = self.repo.get_by_user_and_anime(user_uuid, anime_uuid)

        rating_data = {
            "user": user_uuid,
            "anime": anime_uuid,
            "value": value
        }

        if existing_rating:
            self.repo.update(existing_rating, {"value": value})
            return True

        else:
            self.repo.add(rating_data)

        return False


    def unset_rating(self, user_uuid: str, anime_uuid: str) -> bool:
        existing_rating = self.repo.get_by_user_and_anime(user_uuid, anime_uuid)

        if existing_rating:
            self.repo.delete(existing_rating)
            return True

        return False


    def get_rating(self, user_uuid: str, anime_uuid: str) -> Rating | None:
        return self.repo.get_by_user_and_anime(user_uuid, anime_uuid)

