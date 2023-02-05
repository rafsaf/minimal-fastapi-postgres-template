from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models import User
from app.tests.conftest import (
    default_user_email,
    default_user_id,
    default_user_password_hash,
)


async def test_read_current_user(client: AsyncClient, default_user_headers):
    response = await client.get(
        app.url_path_for("read_current_user"), headers=default_user_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": default_user_id,
        "email": default_user_email,
    }


async def test_delete_current_user(
    client: AsyncClient, default_user_headers, session: AsyncSession
):
    response = await client.delete(
        app.url_path_for("delete_current_user"), headers=default_user_headers
    )
    assert response.status_code == 204
    result = await session.execute(select(User).where(User.id == default_user_id))
    user = result.scalars().first()
    assert user is None


async def test_reset_current_user_password(
    client: AsyncClient, default_user_headers, session: AsyncSession
):
    response = await client.post(
        app.url_path_for("reset_current_user_password"),
        headers=default_user_headers,
        json={"password": "testxxxxxx"},
    )
    assert response.status_code == 200
    result = await session.execute(select(User).where(User.id == default_user_id))
    user = result.scalars().first()
    assert user is not None
    assert user.hashed_password != default_user_password_hash


async def test_register_new_user(
    client: AsyncClient, default_user_headers, session: AsyncSession
):
    response = await client.post(
        app.url_path_for("register_new_user"),
        headers=default_user_headers,
        json={
            "email": "qwe@example.com",
            "password": "asdasdasd",
        },
    )
    assert response.status_code == 200
    result = await session.execute(select(User).where(User.email == "qwe@example.com"))
    user = result.scalars().first()
    assert user is not None
