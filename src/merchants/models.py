import uuid
from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
from .database import Base  # ⬅ pindah ke modul merchants

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(30), nullable=False)
    merchantCategory = Column(String(32), nullable=False)
    imageUrl = Column(String(255), nullable=False)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)
