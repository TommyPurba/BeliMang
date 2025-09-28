from sqlalchemy.orm import Session
from . import models, schemas

def create_merchant(db: Session, payload: schemas.MerchantCreate) -> models.Merchant:
    m = models.Merchant(
        name=payload.name,
        merchantCategory=payload.merchantCategory,
        imageUrl=str(payload.imageUrl),
        lat=payload.Location.Lat,
        long=payload.Location.Long,
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

def list_merchants(db: Session):
    return db.query(models.Merchant).all()
