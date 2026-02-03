import pytest
from fastapi import status
from httpx import AsyncClient

from app.auth.models import User
from app.main import app


@pytest.mark.asyncio(loop_scope="session")
async def test_read_current_user_status_code(
    client: AsyncClient,
    default_user_headers: dict[str, str],
    default_user: User,
) -> None:
    response = await client.get(
        app.url_path_for("read_current_user"),
        headers=default_user_headers,
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio(loop_scope="session")
async def test_read_current_user_response(
    client: AsyncClient,
    default_user_headers: dict[str, str],
    default_user: User,
) -> None:
    response = await client.get(
        app.url_path_for("read_current_user"),
        headers=default_user_headers,
    )

    assert response.json() == {
        "user_id": default_user.user_id,
        "email": default_user.email,
    }
