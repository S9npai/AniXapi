from sqlalchemy import Column, Integer, String, BINARY, Enum, Date, ForeignKey
from sqlalchemy.orm import declarative_base
from utils.uuid_conv import UUIDBinary

Base = declarative_base()

class Anime(Base):
    __tablename__ = "anime"
    uuid = Column(UUIDBinary, primary_key = True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    jp_name = Column(String, nullable=False)
    episodes = Column(Integer)
    format = Column(Enum("TV","movie","OVA","ONA"))
    start_date = Column(Date)
    end_date = Column(Date)
    studio = Column(UUIDBinary, ForeignKey("studios.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
