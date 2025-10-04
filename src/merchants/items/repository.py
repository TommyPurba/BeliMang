# src/merchants/items/repository.py
from __future__ import annotations

from typing import Optional, Tuple, List
from uuid import UUID
from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy import func

from src.merchants.models import Merchant
from .models import Item


def merchant_exists(db: Session, merchant_id: UUID) -> bool:
    """Cek apakah merchant ada di DB."""
    return (
        db.query(Merchant)
        .filter(Merchant.id == merchant_id)
        .limit(1)
        .first()
        is not None
    )


def create_item(db: Session, merchant_id: UUID, data: dict) -> UUID:
    """Insert item baru dan return UUID-nya."""
    # price di schema berupa int; tabel menggunakan Numeric(12,2)
    raw_price = data.get("price")
    price: Optional[Decimal] = None
    if raw_price is not None:
        # str(...) supaya aman untuk Decimal
        price = Decimal(str(raw_price))

    obj = Item(
        merchant_id=merchant_id,
        name=data.get("name"),
        category=data.get("category"),   # sudah dinormalisasi oleh schema (productCategory -> category)
        price=price,
        sku=data.get("sku"),
        description=data.get("description"),
        # imageUrl tidak disimpan (belum ada kolom), jadi diabaikan
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj.id


def list_items(
    db: Session,
    merchant_id: UUID,
    *,
    item_id: Optional[UUID] = None,
    name: Optional[str] = None,
    category: Optional[str] = None,
    created_at: Optional[str] = None,   # "asc" | "desc" | None
    limit: int = 5,
    offset: int = 0,
) -> Tuple[List[Item], int]:
    """
    Ambil list Item + total (untuk meta) dengan filter dan pagination.
    Default sorting created_at desc (sesuai dokumentasi).
    """
    q = db.query(Item).filter(Item.merchant_id == merchant_id)

    if item_id:
        q = q.filter(Item.id == item_id)
    if name:
        q = q.filter(Item.name.ilike(f"%{name}%"))
    if category:
        q = q.filter(Item.category == category)

    # total sebelum limit/offset
    total = q.with_entities(func.count()).scalar() or 0

    if created_at == "asc":
        q = q.order_by(Item.created_at.asc())
    else:
        # default desc
        q = q.order_by(Item.created_at.desc())

    items = q.offset(offset).limit(limit).all()
    return items, int(total)
