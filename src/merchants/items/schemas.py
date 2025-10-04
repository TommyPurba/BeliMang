# src/merchants/items/schemas.py
from datetime import datetime
from typing import Optional, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, AliasChoices, HttpUrl

# Biar DRY: satu alias untuk semua tempat yang butuh kategori valid
ItemCategory = Literal["Beverage", "Food", "Snack", "Condiments", "Additions"]

# ====== Request ======
class ItemCreate(BaseModel):
    # boleh kirim "productCategory" atau "category"
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., min_length=2, max_length=30)
    # internal field = category; input bisa "productCategory"/"category"; output pakai "productCategory"
    category: ItemCategory = Field(
        ...,
        validation_alias=AliasChoices("productCategory", "category"),
        serialization_alias="productCategory",
    )
    price: int = Field(..., ge=1)
    imageUrl: Optional[HttpUrl] = None
    sku: Optional[str] = None
    description: Optional[str] = None


# ====== Response (POST created) ======
class ItemCreated(BaseModel):
    itemId: str


# ====== Response (DETAIL, jika dibutuhkan di endpoint lain) ======
class ItemResponse(BaseModel):
    # alias output: itemId, merchantId, productCategory, createdAt
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    itemId: UUID = Field(validation_alias="id")
    merchantId: UUID = Field(validation_alias="merchant_id")
    name: str
    productCategory: ItemCategory = Field(validation_alias="category")
    price: Optional[float] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    imageUrl: Optional[HttpUrl] = None
    createdAt: datetime = Field(validation_alias="created_at")


# ====== Response (GET list): { data: [...], meta: {...} } ======
class ItemsMeta(BaseModel):
    limit: int
    offset: int
    total: int


class ItemRow(BaseModel):
    # Baris item untuk list; subset field sesuai dokumen
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    itemId: UUID = Field(validation_alias="id")
    name: str
    productCategory: ItemCategory = Field(validation_alias="category")
    price: Optional[float] = None
    imageUrl: Optional[HttpUrl] = None
    createdAt: datetime = Field(validation_alias="created_at")


class ItemsListResponse(BaseModel):
    data: list[ItemRow]
    meta: ItemsMeta


# ====== Error ======
class ErrorResponse(BaseModel):
    error: str
    message: str
