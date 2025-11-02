"""Shared FastAPI dependencies."""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import get_db
from .models import User


def db_session() -> Session:
    """Provide a synchronous SQLAlchemy session."""

    yield from get_db()


def get_current_user(db: Session = Depends(db_session)) -> User:
    """Placeholder dependency for authenticated user.

    In a production system, this would verify tokens. Here, we fetch the first
    user in the database or raise an error, providing a simplified approach for
    demo purposes.
    """

    user = db.query(User).filter(User.is_active.is_(True)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No active user available. Please seed the database with a user.",
        )
    return user
