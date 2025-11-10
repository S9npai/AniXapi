from sqlalchemy import Column, String, BINARY, Enum, TIMESTAMP
from sqlalchemy import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    uuid = Column(BINARY, primary_key=True, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    role = Column(Enum("user","admin"), default="user")
