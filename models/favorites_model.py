from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Favorites(Base):
    __tablename__ = "favorites"
    user = Column(ForeignKey("users.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    anime = Column(ForeignKey("anime.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint ("user","anime")
    )

