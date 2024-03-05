from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models import User


async def test_delete_current_user_status_code(
    client: AsyncClient,
    default_user_headers: dict[str, str],
) -> None:
    response = await client.delete(
        app.url_path_for("delete_current_user"),
        headers=default_user_headers,
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_delete_current_user_is_deleted_in_db(
    client: AsyncClient,
    default_user_headers: dict[str, str],
    default_user: User,
    session: AsyncSession,
) -> None:
    await client.delete(
        app.url_path_for("delete_current_user"),
        headers=default_user_headers,
    )

    user = await session.scalar(
        select(User).where(User.user_id == default_user.user_id)
    )
    assert user is None
