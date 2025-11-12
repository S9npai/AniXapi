from sqlalchemy import Column, Integer, String, Enum, Date
from sqlalchemy.orm import declarative_base, relationship

from models.favorites_model import Favorites
from models.studio_anime_model import anime_studio_association
from utils.uuid_conv import UUIDBinary
from models.BaseModel import Base

class Anime(Base):
    __tablename__ = "anime"
    uuid = Column(UUIDBinary, primary_key=True, nullable=False, unique=True)
    name = Column(String, unique=True, nullable=False)
    jp_name = Column(String, nullable=False)
    episodes = Column(Integer)
    format = Column(Enum("TV","movie","OVA","ONA"))
    start_date = Column(Date)
    end_date = Column(Date)

    favorited_by = relationship(
        "User",
        secondary=Favorites.__tablename__,
        back_populates="favorites"
    )

    studios = relationship(
        "Studio",
        secondary=anime_studio_association,
        back_populates="animes"
    )
