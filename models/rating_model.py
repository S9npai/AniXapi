from sqlalchemy import Column, ForeignKey, Float, PrimaryKeyConstraint, CheckConstraint
from sqlalchemy.orm import relationship

from BaseModel import Base
from utils.uuid_conv import UUIDBinary


class Rating(Base):
    __tablename__ = "ratings"
    anime = Column(UUIDBinary, ForeignKey("anime.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user = Column(UUIDBinary, ForeignKey("users.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    value = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint ("user","anime")
    )

    user_rel = relationship("User", back_populates="ratings")
    anime_rel = relationship("Anime", back_populates="ratings")

