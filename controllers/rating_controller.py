from sqlalchemy import and_
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from models.rating_model import Rating
from schemas.rating_validator import RatingValidator
from utils.uuid_conv import uuid_to_binary


def set_rating(db: Session, user_id: str, anime_id: str, value: float) -> RatingValidator:
    result = db.execute(
        update(Rating).where((Rating.user == user_id) &
        (Rating.anime == anime_id)).values(value=value))

    if result.rowcount > 0:
        db.commit()
        return {"status": "success", "message": "Rating updated"}

    try:
        new_rating = Rating(user=user_id, anime=anime_id, value=value)
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)

        return RatingValidator.model_validate(new_rating)

    except (IntegrityError, Exception):
        db.rollback()
        return {"status": "error", "message": "Invalid user or anime UUIDs"}, 400


def delete_rating(db: Session, user_uuid: str, anime_uuid: str) -> None:
    rating_to_delete = db.query(RatingValidator).get((user_uuid, anime_uuid))

    if not rating_to_delete:
        raise Exception("Rating not found.")

    db.delete(rating_to_delete)
    db.commit()


def get_rating(db:Session, user_uuid: str, anime_uuid: str):
    binary_user_uuid = uuid_to_binary(user_uuid)
    binary_anime_uuid = uuid_to_binary(anime_uuid)

    rating = db.execute(
        select(Rating).where(
            and_ (Rating.user == binary_user_uuid,
                  Rating.anime == binary_anime_uuid)
        )
    ).scalar_one_or_none()

    if not rating:
        return None, "The anime is unrated by that user !"

    return RatingValidator.model_validate(rating)

