from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.password import verify_password
from app.main import app
from app.models import User


async def test_reset_current_user_password_status_code(
    client: AsyncClient,
    default_user_headers: dict[str, str],
) -> None:
    response = await client.post(
        app.url_path_for("reset_current_user_password"),
        headers=default_user_headers,
        json={"password": "test_pwd"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_reset_current_user_password_is_changed_in_db(
    client: AsyncClient,
    default_user_headers: dict[str, str],
    default_user: User,
    session: AsyncSession,
) -> None:
    await client.post(
        app.url_path_for("reset_current_user_password"),
        headers=default_user_headers,
        json={"password": "test_pwd"},
    )

    user = await session.scalar(
        select(User).where(User.user_id == default_user.user_id)
    )
    assert user is not None
    assert verify_password("test_pwd", user.hashed_password)
