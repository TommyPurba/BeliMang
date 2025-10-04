# src/merchants/service.py
from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
import uuid

from . import models, schemas


def create_merchant(db: Session, payload: schemas.MerchantCreate) -> models.Merchant:
    m = models.Merchant(
        name=payload.name,
        merchantCategory=payload.merchantCategory,
        imageUrl=str(payload.imageUrl),
        lat=payload.Location.Lat,
        long=payload.Location.Long,   # geog auto (computed)
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


def list_merchants(
    db: Session,
    merchant_id: Optional[str] = None,
    name: Optional[str] = None,
    category: Optional[str] = None,
    sort_created_at: Optional[str] = None,  # "asc" | "desc" | None
    limit: int = 5,
    offset: int = 0,
):
    """
    Return:
      items: List[dict] yang cocok ke schemas.MerchantRead
      total: int
    """
    query = db.query(models.Merchant)

    # filter by merchant_id (UUID)
    if merchant_id:
        try:
            merchant_uuid = uuid.UUID(merchant_id)
            query = query.filter(models.Merchant.id == merchant_uuid)
        except (ValueError, AttributeError):
            return [], 0  # kalau format ID invalid → kosong

    # filter by name (case-insensitive, wildcard)
    if name:
        query = query.filter(models.Merchant.name.ilike(f"%{name}%"))

    # filter by category
    if category:
        query = query.filter(models.Merchant.merchantCategory == category)

    # sorting by createdAt
    if sort_created_at == "asc":
        query = query.order_by(asc(models.Merchant.createdAt))
    elif sort_created_at == "desc":
        query = query.order_by(desc(models.Merchant.createdAt))

    total = query.count()
    rows: List[models.Merchant] = query.limit(limit).offset(offset).all()

    # mapping ke bentuk yang cocok dengan Pydantic schema (MerchantRead)
    items = [
        {
            "merchantId": str(r.id),
            "name": r.name,
            "merchantCategory": r.merchantCategory,
            "imageUrl": r.imageUrl,
            "Location": {"Lat": r.lat, "Long": r.long},
            "createdAt": r.createdAt,
        }
        for r in rows
    ]

    return items, total
