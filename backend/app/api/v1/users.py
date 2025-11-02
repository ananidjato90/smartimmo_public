"""User management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ... import schemas
from ...dependencies import db_session
from ...models import User
from ...security import get_password_hash, verify_password


router = APIRouter(prefix="/users")


@router.post("", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(*, user_in: schemas.UserCreate, db: Session = Depends(db_session)) -> User:
    """Create a new user in the system."""

    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        phone_number=user_in.phone_number,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(db_session)) -> list[User]:
    """Return all users."""

    return db.query(User).order_by(User.created_at.desc()).all()


@router.post("/login", response_model=schemas.UserRead)
def login_user(
    *,
    credentials: schemas.UserLogin,
    db: Session = Depends(db_session),
) -> User:
    """Authenticate a user. (Simplified for demonstration)"""

    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return user
