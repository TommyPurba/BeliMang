# src/merchants/router.py
from typing import Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from .database import get_db
from . import schemas, service
from .dependencies import get_current_admin

# import items router
from src.merchants.items.router import router as items_router

router = APIRouter(
    prefix="/admin/merchants",
    tags=["Merchants"]
)

# === POST /admin/merchants ====================================================
@router.post(
    "/", 
    response_model=schemas.MerchantOut, 
    status_code=status.HTTP_201_CREATED
)
def add_merchant(
    payload: schemas.MerchantCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_admin),
):
    """Tambah merchant baru"""
    m = service.create_merchant(db, payload)
    return {"merchantId": str(m.id)}


# === GET /admin/merchants =====================================================
VALID_CATEGORIES = {
    "SmallRestaurant",
    "MediumRestaurant",
    "LargeRestaurant",
    "MerchandiseRestaurant",
    "BoothKiosk",
    "ConvenienceStore",
}
VALID_CREATED_AT_SORT = {"asc", "desc"}

@router.get(
    "/", 
    response_model=schemas.MerchantListResponse, 
    status_code=status.HTTP_200_OK
)
def list_merchants(
    merchantId: Optional[str] = None,
    limit: int = Query(default=5, ge=1),
    offset: int = Query(default=0, ge=0),
    name: Optional[str] = None,
    merchantCategory: Optional[str] = None,
    createdAt: Optional[str] = None,  # "asc" | "desc"
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_admin),
):
    """
    List merchants dengan filter:
    - Semua param opsional
    - name: wildcard, case-insensitive
    - merchantCategory: enum; jika invalid -> return kosong
    - createdAt: 'asc' / 'desc'; jika salah -> diabaikan
    - merchantId tidak ketemu -> return kosong
    """

    if merchantCategory and merchantCategory not in VALID_CATEGORIES:
        return {"data": [], "meta": {"limit": limit, "offset": offset, "total": 0}}

    sort_dir = createdAt if createdAt in VALID_CREATED_AT_SORT else None

    items, total = service.list_merchants(
        db=db,
        merchant_id=merchantId,
        name=name,
        category=merchantCategory,
        sort_created_at=sort_dir,
        limit=limit,
        offset=offset,
    )

    return {"data": items, "meta": {"limit": limit, "offset": offset, "total": total}}



router.include_router(
    items_router,
    prefix="/{merchant_id}/items",
    tags=["Admin - Items"]   
)
