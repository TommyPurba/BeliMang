import uuid
from sqlalchemy import Column, String, Float, Computed, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from geoalchemy2 import Geography
from .database import Base


class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(30), nullable=False)
    merchantCategory = Column(String(32), nullable=False)
    imageUrl = Column(String(255), nullable=False)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)

    # POINT(lon lat), SRID 4326, dihasilkan otomatis dari kolom long/lat
    geog = Column(
        Geography(geometry_type="POINT", srid=4326),
        Computed("ST_SetSRID(ST_MakePoint(long, lat), 4326)::geography", persisted=True),
        nullable=False,
    )

    # waktu pembuatan record
    createdAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
