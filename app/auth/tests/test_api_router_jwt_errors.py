import pytest
from fastapi import status
from freezegun import freeze_time
from httpx import AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import api_messages
from app.auth.jwt import create_jwt_token
from app.auth.models import User
from app.main import app


@pytest.mark.asyncio(loop_scope="session")
async def test_api_raise_401_on_jwt_decode_errors(
    client: AsyncClient,
) -> None:
    response = await client.get(
        app.url_path_for("read_current_user"),
        headers={"Authorization": "Bearer garbage-invalid-jwt"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text
    assert response.json() == {"detail": "Token invalid: Not enough segments"}


@pytest.mark.asyncio(loop_scope="session")
async def test_api_raise_401_on_jwt_expired_token(
    client: AsyncClient,
    default_user: User,
) -> None:
    with freeze_time("2023-01-01"):
        jwt = create_jwt_token(default_user.user_id)
    with freeze_time("2023-02-01"):
        response = await client.get(
            app.url_path_for("read_current_user"),
            headers={"Authorization": f"Bearer {jwt.access_token}"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text
        assert response.json() == {"detail": "Token invalid: Signature has expired"}


@pytest.mark.asyncio(loop_scope="session")
async def test_api_raise_401_on_jwt_user_deleted(
    client: AsyncClient,
    default_user_headers: dict[str, str],
    default_user: User,
    session: AsyncSession,
) -> None:
    await session.execute(delete(User).where(User.user_id == default_user.user_id))
    await session.commit()

    response = await client.get(
        app.url_path_for("read_current_user"),
        headers=default_user_headers,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text
    assert response.json() == {"detail": api_messages.JWT_ERROR_USER_REMOVED}
