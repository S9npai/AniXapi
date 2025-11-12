from sqlalchemy import Column, Table, ForeignKey
from models.BaseModel import Base

anime_studio_association = Table(
    "anime_studio_association",
    Base.metadata,
    Column("anime_uuid", ForeignKey("anime.uuid", ondelete="CASCADE"), primary_key=True),
    Column("studio_uuid", ForeignKey("studios.uuid", ondelete="CASCADE"), primary_key=True),
)
