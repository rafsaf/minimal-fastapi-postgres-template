import logging
from typing import Optional

from sqlalchemy import select

from app.core import security
from app.core.config import settings
from app.models import User
from app.session import async_session
from asyncio import get_event_loop


async def main() -> None:
    logging.info("Start initial data")
    async with async_session() as session:

        result = await session.execute(
            select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
        )
        user: Optional[User] = result.scalars().first()

        if user is None:
            new_superuser = User(
                email=settings.FIRST_SUPERUSER_EMAIL,
                hashed_password=security.get_password_hash(
                    settings.FIRST_SUPERUSER_PASSWORD
                ),
                full_name=settings.FIRST_SUPERUSER_EMAIL,
            )
            session.add(new_superuser)
            await session.commit()
            logging.info("Superuser was created")
        else:
            logging.warning("Superuser already exists in database")

        logging.info("Initial data created")


if __name__ == "__main__":
    get_event_loop().run_until_complete(main())
