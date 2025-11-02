"""Security helpers for password hashing and verification."""

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Return a hashed password."""

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check whether the provided password matches the hash."""

    return pwd_context.verify(plain_password, hashed_password)
