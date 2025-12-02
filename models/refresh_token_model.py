from sqlalchemy import Column, ForeignKey, DateTime, Boolean, String, func
from sqlalchemy.orm import relationship
from models.BaseModel import Base
from utils.uuid_conv import UUIDBinary


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(UUIDBinary, primary_key=True, unique=True, nullable=False)
    user_uuid = Column(UUIDBinary, ForeignKey('users.uuid', ondelete='CASCADE'), nullable=False)
    issued_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)


    user = relationship(
        "User",
        back_populates="refresh_tokens"
    )

