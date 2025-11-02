"""Pydantic schemas for request and response validation."""

from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field

from .models import PropertyStatus, PropertyType


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: str | None = None


class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=8)]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PropertyImageBase(BaseModel):
    url: str
    is_primary: bool = False


class PropertyImageCreate(PropertyImageBase):
    pass


class PropertyImageRead(PropertyImageBase):
    id: int

    class Config:
        from_attributes = True


class PropertyBase(BaseModel):
    title: str
    description: str
    price: float
    area: float | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    city: str
    district: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    property_type: PropertyType
    status: PropertyStatus = PropertyStatus.AVAILABLE
    is_featured: bool = False


class PropertyCreate(PropertyBase):
    images: list[PropertyImageCreate] | None = None


class PropertyUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    area: float | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    city: str | None = None
    district: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    property_type: PropertyType | None = None
    status: PropertyStatus | None = None
    is_featured: bool | None = None
    images: list[PropertyImageCreate] | None = None


class PropertyRead(PropertyBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    images: list[PropertyImageRead] = Field(default_factory=list)

    class Config:
        from_attributes = True


class FavoriteRead(BaseModel):
    id: int
    property: PropertyRead
    created_at: datetime

    class Config:
        from_attributes = True
