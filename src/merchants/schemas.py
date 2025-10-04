from pydantic import BaseModel, Field, HttpUrl
from typing import Literal, List, Optional
from datetime import datetime


class LocationSchema(BaseModel):
    Lat: float = Field(..., description="Latitude")
    Long: float = Field(..., description="Longitude")


class MerchantCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=30)
    merchantCategory: Literal[
        "SmallRestaurant", "MediumRestaurant", "LargeRestaurant",
        "MerchandiseRestaurant", "BoothKiosk", "ConvenienceStore"
    ]
    imageUrl: HttpUrl
    Location: LocationSchema


class MerchantOut(BaseModel):
    merchantId: str


# === untuk GET /admin/merchants ===
class MerchantRead(BaseModel):
    merchantId: str
    name: str
    merchantCategory: str
    imageUrl: Optional[HttpUrl]
    Location: LocationSchema
    createdAt: datetime   # ISO 8601 format otomatis dari Pydantic

    class Config:
        orm_mode = True   # biar bisa langsung parse dari SQLAlchemy object


class MetaSchema(BaseModel):
    limit: int
    offset: int
    total: int


class MerchantListResponse(BaseModel):
    data: List[MerchantRead]
    meta: MetaSchema
