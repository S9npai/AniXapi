from sqlalchemy import Column, String, Enum, TIMESTAMP
from sqlalchemy import func
from sqlalchemy.orm import relationship

from models.favorites_model import Favorites
from utils.uuid_conv import UUIDBinary
from models.BaseModel import Base

class User(Base):
    __tablename__ = "users"
    uuid = Column(UUIDBinary, primary_key=True, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    role = Column(Enum("user","admin"), default="user")

    favorites = relationship(
        "Anime",
        secondary=Favorites.__tablename__,
        back_populates="favorited_by"
    )
