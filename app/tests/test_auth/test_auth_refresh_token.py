import time

from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models import RefreshToken, User


async def test_refresh_token_fails_with_message_when_token_does_not_exist(
    client: AsyncClient,
) -> None:
    response = await client.post(
        app.url_path_for("refresh_token"),
        json={
            "refresh_token": "blaxx",
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Token not found"}


async def test_refresh_token_fails_with_message_when_token_is_expired(
    client: AsyncClient,
    default_user: User,
    session: AsyncSession,
) -> None:
    test_refresh_token = RefreshToken(
        user_id=default_user.user_id,
        refresh_token="blaxx",
        exp=int(time.time()) - 1,
    )
    session.add(test_refresh_token)
    await session.commit()

    response = await client.post(
        app.url_path_for("refresh_token"),
        json={
            "refresh_token": "blaxx",
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Token not found"}


async def test_refresh_token_fails_with_message_when_token_is_used(
    client: AsyncClient,
    default_user: User,
    session: AsyncSession,
) -> None:
    test_refresh_token = RefreshToken(
        user_id=default_user.user_id,
        refresh_token="blaxx",
        exp=int(time.time()) + 1000,
        used=True,
    )
    session.add(test_refresh_token)
    await session.commit()

    response = await client.post(
        app.url_path_for("refresh_token"),
        json={
            "refresh_token": "blaxx",
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Token not found"}
