from sqlalchemy import Column, ForeignKey, Float, PrimaryKeyConstraint, CheckConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Rating(Base):
    __tablename__ = "ratings"
    anime = Column(ForeignKey("anime.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user = Column(ForeignKey("users.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    value = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint ("user","anime"),
        CheckConstraint('value >=0 AND value <= 5', name='rating_value_check')
    )

