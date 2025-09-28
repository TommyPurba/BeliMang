# src/merchants/router.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from .database import get_db        # DB module di merchants
from . import schemas, service      # schemas.py & service.py di merchants

router = APIRouter(prefix="/admin/merchants", tags=["Merchants"])

@router.post("/", response_model=schemas.MerchantOut, status_code=status.HTTP_201_CREATED)
def add_merchant(payload: schemas.MerchantCreate, db: Session = Depends(get_db)):
    m = service.create_merchant(db, payload)
    return {"merchantId": str(m.id)}

@router.get("/", response_model=List[schemas.MerchantListItem])
def get_merchants(db: Session = Depends(get_db)):
    items = service.list_merchants(db)
    return [
        {
            "merchantId": str(i.id),
            "name": i.name,
            "merchantCategory": i.merchantCategory,
            "imageUrl": i.imageUrl,   # <- fixed key
            "lat": i.lat,
            "long": i.long,
        }
        for i in items
    ]
