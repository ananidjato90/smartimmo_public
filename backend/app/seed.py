"""Utility script to populate the database with demo data."""

from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from .models import Property, PropertyImage, PropertyStatus, PropertyType, User, init_db
from .security import get_password_hash


def seed() -> None:
    init_db(engine)
    db: Session = SessionLocal()
    try:
        if db.query(User).count() > 0:
            return

        user = User(
            email="demo@smartimmo.tg",
            full_name="Agent D?mo",
            phone_number="+22890000000",
            hashed_password=get_password_hash("DemoPass123!"),
            is_superuser=True,
        )
        db.add(user)
        db.flush()

        properties = [
            Property(
                title="Appartement moderne ? Lom?",
                description="Appartement de 3 chambres climatis?es, proche du centre-ville.",
                price=350000,
                area=120,
                bedrooms=3,
                bathrooms=2,
                city="Lom?",
                district="Tokoin",
                property_type=PropertyType.APARTMENT,
                status=PropertyStatus.AVAILABLE,
                owner_id=user.id,
                images=[
                    PropertyImage(
                        url="https://images.unsplash.com/photo-1505691938895-1758d7feb511",
                        is_primary=True,
                    )
                ],
            ),
            Property(
                title="Villa contemporaine avec piscine",
                description="Villa haut standing avec piscine, jardin et garage.",
                price=95000000,
                area=420,
                bedrooms=5,
                bathrooms=4,
                city="Lom?",
                district="Ago?",
                property_type=PropertyType.HOUSE,
                status=PropertyStatus.AVAILABLE,
                owner_id=user.id,
                images=[
                    PropertyImage(
                        url="https://images.unsplash.com/photo-1505691723518-36a5ac3be353",
                        is_primary=True,
                    )
                ],
            ),
            Property(
                title="Terrain constructible ? Kpalim?",
                description="Terrain viabilis? de 800 m? id?al pour un projet r?sidentiel.",
                price=18000000,
                area=800,
                city="Kpalim?",
                property_type=PropertyType.LAND,
                status=PropertyStatus.AVAILABLE,
                owner_id=user.id,
                images=[
                    PropertyImage(
                        url="https://images.unsplash.com/photo-1523287562758-66c7fc58967d",
                        is_primary=True,
                    )
                ],
            ),
        ]

        db.add_all(properties)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
