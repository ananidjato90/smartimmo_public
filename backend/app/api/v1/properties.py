"""Property endpoints for the Togo Real Estate API."""

from collections.abc import Sequence
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ... import schemas
from ...dependencies import db_session, get_current_user
from ...models import Property, PropertyImage, PropertyStatus, PropertyType, User


router = APIRouter(prefix="/properties")


@router.get("", response_model=list[schemas.PropertyRead])
def list_properties(
    *,
    db: Session = Depends(db_session),
    city: str | None = Query(default=None, description="Filter by city name"),
    property_type: PropertyType | None = Query(default=None),
    status: PropertyStatus | None = Query(default=None),
    min_price: float | None = Query(default=None),
    max_price: float | None = Query(default=None),
    bedrooms: int | None = Query(default=None),
    bathrooms: int | None = Query(default=None),
    is_featured: bool | None = Query(default=None),
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0, ge=0),
) -> Sequence[Property]:
    """Return a filtered list of properties."""

    query = db.query(Property).order_by(Property.created_at.desc())

    if city:
        query = query.filter(Property.city.ilike(f"%{city}%"))
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if status:
        query = query.filter(Property.status == status)
    if min_price is not None:
        query = query.filter(Property.price >= min_price)
    if max_price is not None:
        query = query.filter(Property.price <= max_price)
    if bedrooms is not None:
        query = query.filter(Property.bedrooms >= bedrooms)
    if bathrooms is not None:
        query = query.filter(Property.bathrooms >= bathrooms)
    if is_featured is not None:
        query = query.filter(Property.is_featured.is_(is_featured))

    return query.offset(offset).limit(limit).all()


@router.post("", response_model=schemas.PropertyRead, status_code=status.HTTP_201_CREATED)
def create_property(
    *,
    property_in: schemas.PropertyCreate,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
) -> Property:
    """Create a new property listing."""

    property_obj = Property(
        **property_in.model_dump(exclude={"images"}),
        owner_id=current_user.id,
    )

    if property_in.images:
        property_obj.images = [
            PropertyImage(**image.model_dump()) for image in property_in.images
        ]

    db.add(property_obj)
    db.commit()
    db.refresh(property_obj)
    return property_obj


@router.get("/{property_id}", response_model=schemas.PropertyRead)
def get_property(
    *,
    property_id: int,
    db: Session = Depends(db_session),
) -> Property:
    """Retrieve a single property by its identifier."""

    property_obj = db.get(Property, property_id)
    if not property_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return property_obj


@router.put("/{property_id}", response_model=schemas.PropertyRead)
def update_property(
    *,
    property_id: int,
    property_in: schemas.PropertyUpdate,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
) -> Property:
    """Update an existing property."""

    property_obj = db.get(Property, property_id)
    if not property_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    if property_obj.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this property")

    for field, value in property_in.model_dump(
        exclude_unset=True, exclude={"images"}
    ).items():
        setattr(property_obj, field, value)

    if property_in.images is not None:
        property_obj.images.clear()
        for image in property_in.images:
            property_obj.images.append(PropertyImage(**image.model_dump()))

    db.add(property_obj)
    db.commit()
    db.refresh(property_obj)
    return property_obj


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(
    *,
    property_id: int,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
) -> None:
    """Remove a property listing."""

    property_obj = db.get(Property, property_id)
    if not property_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    if property_obj.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this property")

    db.delete(property_obj)
    db.commit()
