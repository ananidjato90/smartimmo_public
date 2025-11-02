"""Version 1 API router combining individual endpoints."""

from fastapi import APIRouter

from . import properties, users, favorites, ai


router = APIRouter(prefix="/api/v1")

router.include_router(properties.router, tags=["properties"])
router.include_router(users.router, tags=["users"])
router.include_router(favorites.router, tags=["favorites"])
router.include_router(ai.router, tags=["ai"])


__all__ = ["router"]
