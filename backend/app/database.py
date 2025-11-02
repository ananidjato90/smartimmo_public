"""Database session and engine configuration."""

from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import get_settings


settings = get_settings()

DATABASE_URL = (
    f"mysql+pymysql://{settings.mysql_user}:{settings.mysql_password}"
    f"@{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_database}"
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.environment == "development",
    future=True,
)


SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)


def get_db() -> Generator:
    """Yield a SQLAlchemy session, ensuring proper cleanup."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
