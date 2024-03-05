from fastapi import status
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import api_messages
from app.main import app
from app.models import User


async def test_register_new_user_status_code(
    client: AsyncClient,
) -> None:
    response = await client.post(
        app.url_path_for("register_new_user"),
        json={
            "email": "test@email.com",
            "password": "testtesttest",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED


async def test_register_new_user_creates_record_in_db(
    client: AsyncClient,
    session: AsyncSession,
) -> None:
    await client.post(
        app.url_path_for("register_new_user"),
        json={
            "email": "test@email.com",
            "password": "testtesttest",
        },
    )

    user_count = await session.scalar(
        select(func.count()).where(User.email == "test@email.com")
    )
    assert user_count == 1


async def test_register_new_user_cannot_create_already_created_user(
    client: AsyncClient,
    session: AsyncSession,
) -> None:
    user = User(
        email="test@email.com",
        hashed_password="bla",
    )
    session.add(user)
    await session.commit()

    response = await client.post(
        app.url_path_for("register_new_user"),
        json={
            "email": "test@email.com",
            "password": "testtesttest",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": api_messages.EMAIL_ADDRESS_ALREADY_USED}
