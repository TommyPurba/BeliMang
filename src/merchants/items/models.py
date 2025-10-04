import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.merchants.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    merchant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("merchants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name = Column(String(100), nullable=False, index=True)
    category = Column(String(32), nullable=False, index=True)  # "Beverage", "Food", dll
    price = Column(Numeric(12, 2), nullable=True)
    sku = Column(String(64), nullable=True, index=True)
    description = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
