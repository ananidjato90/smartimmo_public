"""Favorites endpoints for user saved properties."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ... import schemas
from ...dependencies import db_session, get_current_user
from ...models import Favorite, Property, User


router = APIRouter(prefix="/favorites")


@router.get("", response_model=list[schemas.FavoriteRead])
def list_favorites(
    *,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
) -> list[Favorite]:
    """Return the authenticated user's favorite properties."""

    favorites = (
        db.query(Favorite)
        .filter(Favorite.user_id == current_user.id)
        .order_by(Favorite.created_at.desc())
        .all()
    )
    return favorites


@router.post("/{property_id}", response_model=schemas.FavoriteRead, status_code=status.HTTP_201_CREATED)
def add_favorite(
    *,
    property_id: int,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
) -> Favorite:
    """Create a favorite link between the user and a property."""

    property_obj = db.get(Property, property_id)
    if not property_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")

    existing = (
        db.query(Favorite)
        .filter(Favorite.user_id == current_user.id, Favorite.property_id == property_id)
        .first()
    )
    if existing:
        return existing

    favorite = Favorite(user_id=current_user.id, property_id=property_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    *,
    property_id: int,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
) -> None:
    """Remove the property from favorites."""

    favorite = (
        db.query(Favorite)
        .filter(Favorite.user_id == current_user.id, Favorite.property_id == property_id)
        .first()
    )
    if not favorite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")

    db.delete(favorite)
    db.commit()
