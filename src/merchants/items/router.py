# src/merchants/items/router.py
from __future__ import annotations

from enum import Enum
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.merchants.database import get_db
from src.merchants.dependencies import get_current_admin
from . import repository as repo
from .schemas import (
    ItemCreate,
    ItemCreated,
    ItemsListResponse,
    ErrorResponse,
    ItemCategory,  # Literal union dari schemas
)

router = APIRouter(tags=["Admin - Items"])  # prefix datang dari merchants/router.py


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


# =========================
# POST /admin/merchants/{merchant_id}/items
# =========================
@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ItemCreated,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Merchant Not Found"},
    },
)
def create_item_for_merchant(
    merchant_id: UUID,            # dari prefix di merchants/router.py
    payload: ItemCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    # 404 kalau merchant tidak ada
    if not repo.merchant_exists(db, merchant_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "NotFound", "message": f"Merchant with id '{merchant_id}' not found"},
        )

    # Penting: JANGAN by_alias, supaya key 'category' (bukan 'productCategory') yang dikirim ke repo
    new_id = repo.create_item(db, merchant_id, data=payload.model_dump())
    return {"itemId": str(new_id)}


# =========================
# GET /admin/merchants/{merchant_id}/items
# =========================
@router.get(
    "",
    response_model=ItemsListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Merchant Not Found"},
    },
    summary="Get items of a merchant with optional filters",
)
def get_items_for_merchant(
    merchant_id: UUID,
    item_id: Optional[UUID] = Query(None, alias="itemId", description="Filter by item id"),
    limit: int = Query(5, ge=1, description="Limit"),
    offset: int = Query(0, ge=0, description="Offset"),
    name: Optional[str] = Query(None, description="Filter by name (ILIKE)"),
    product_category: Optional[ItemCategory] = Query(None, alias="productCategory", description="Filter by product category"),
    created_at: Optional[SortOrder] = Query(None, alias="createdAt", description="Sort by created time (asc|desc)"),
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    # 404 kalau merchant tidak ada
    if not repo.merchant_exists(db, merchant_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "NotFound", "message": f"Merchant with id '{merchant_id}' not found"},
        )

    # Normalisasi input untuk repo
    sort = created_at.value if created_at else None
    category = str(product_category) if product_category else None

    # Query ke repo (mengembalikan (items, total))
    items, total = repo.list_items(
        db,
        merchant_id=merchant_id,
        item_id=item_id,
        name=name,
        category=category,
        created_at=sort,
        limit=limit,
        offset=offset,
    )

    # Pydantic akan map ORM -> ItemRow dengan alias (itemId, productCategory, createdAt)
    return {"data": items, "meta": {"limit": limit, "offset": offset, "total": total}}
