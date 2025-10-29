import sqlalchemy
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint

Base = declarative_base()

class Favorites(Base):
    __tablename__ = "favorites"
    user = Column(ForeignKey("users.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    anime = Column(ForeignKey("anime.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint ("user","anime")
    )

