from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from utils.uuid_conv import UUIDBinary
from models.studio_anime_model import anime_studio_association
from models.BaseModel import Base

class Studio(Base):
    __tablename__ = "studios"
    uuid = Column(UUIDBinary, primary_key = True, nullable=False)
    name = Column(String, unique=True, nullable=False)

    animes = relationship(
        "Anime",
        secondary=anime_studio_association,
        back_populates="studios"
    )
