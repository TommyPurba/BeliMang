from pydantic import BaseModel, Field, HttpUrl
from typing import Literal

class LocationSchema(BaseModel):
    Lat: float = Field(..., description="Latitude")
    Long: float = Field(..., description="Longitude")

class MerchantCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=30)
    merchantCategory: Literal[
        "SmallRestaurant",
        "MediumRestaurant",
        "LargeRestaurant",
        "MerchandiseRestaurant",
        "BoothKiosk",
        "ConvenienceStore",
    ]
    imageUrl: HttpUrl
    Location: LocationSchema

class MerchantOut(BaseModel):
    merchantId: str

class MerchantListItem(BaseModel):
    merchantId: str
    name: str
    merchantCategory: str
    imageUrl: str
    lat: float
    long: float
