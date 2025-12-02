from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint
from models.BaseModel import Base

class Favorites(Base):
    __tablename__ = "favorites"
    user = Column(ForeignKey("users.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    anime = Column(ForeignKey("anime.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    __mapper_args__ = {
            "primary_key": [user, anime]  # explicitly tell SQLAlchemy the PK columns
        }
