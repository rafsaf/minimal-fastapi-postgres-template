import logging

from sqlalchemy import select

from app.core import security
from app.core.config import settings
from app.models import User
from app.session import SessionLocal


def main() -> None:
    logging.info("Start initial data")
    session = SessionLocal()
    user = (
        session.execute(
            select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
        )
        .scalars()
        .first()
    )

    if user is None:
        new_superuser = User(
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=security.get_password_hash(
                settings.FIRST_SUPERUSER_PASSWORD
            ),
            full_name=settings.FIRST_SUPERUSER_EMAIL,
        )
        session.add(new_superuser)
        session.commit()
        logging.info("Superuser was created")
    else:
        logging.warning("Superuser already exists in database")

    logging.info("Initial data created")


if __name__ == "__main__":
    main()
