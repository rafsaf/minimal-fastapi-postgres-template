import time

from fastapi import status
from freezegun import freeze_time
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import api_messages
from app.core.config import get_settings
from app.core.security.jwt import verify_jwt_token
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
    assert response.json() == {"detail": api_messages.REFRESH_TOKEN_NOT_FOUND}


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

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": api_messages.REFRESH_TOKEN_EXPIRED}


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

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": api_messages.REFRESH_TOKEN_ALREADY_USED}


async def test_refresh_token_success_response_status_code(
    client: AsyncClient,
    default_user: User,
    session: AsyncSession,
) -> None:
    test_refresh_token = RefreshToken(
        user_id=default_user.user_id,
        refresh_token="blaxx",
        exp=int(time.time()) + 1000,
        used=False,
    )
    session.add(test_refresh_token)
    await session.commit()

    response = await client.post(
        app.url_path_for("refresh_token"),
        json={
            "refresh_token": "blaxx",
        },
    )

    assert response.status_code == status.HTTP_200_OK


async def test_refresh_token_success_old_token_is_used(
    client: AsyncClient,
    default_user: User,
    session: AsyncSession,
) -> None:
    test_refresh_token = RefreshToken(
        user_id=default_user.user_id,
        refresh_token="blaxx",
        exp=int(time.time()) + 1000,
        used=False,
    )
    session.add(test_refresh_token)
    await session.commit()

    await client.post(
        app.url_path_for("refresh_token"),
        json={
            "refresh_token": "blaxx",
        },
    )

    used_test_refresh_token = await session.scalar(
        select(RefreshToken).where(RefreshToken.refresh_token == "blaxx")
    )
    assert used_test_refresh_token is not None
    assert used_test_refresh_token.used


async def test_refresh_token_success_jwt_has_valid_token_type(
    client: AsyncClient,
    default_user: User,
    session: AsyncSession,
) -> None:
    test_refresh_token = RefreshToken(
        user_id=default_user.user_id,
        refresh_token="blaxx",
        exp=int(time.time()) + 1000,
        used=False,
    )
    session.add(test_refresh_token)
    await session.commit()

    response = await client.post(
        app.url_path_for("refresh_token"),
        json={
            "refresh_token": "blaxx",
        },
    )

    token = response.json()
    assert token["token_type"] == "Bearer"


@freeze_time("2023-01-01")
async def test_refresh_token_success_jwt_has_valid_expire_time(
    client: AsyncClient,
    default_user: User,
    session: AsyncSession,
) -> None:
    test_refresh_token = RefreshToken(
        user_id=default_user.user_id,
        refresh_token="blaxx",
        exp=int(time.time()) + 1000,
        used=False,
    )
    session.add(test_refresh_token)
    await session.commit()

    response = await client.post(
        app.url_path_for("refresh_token"),
        json={
            "refresh_token": "blaxx",
        },
    )

    token = response.json()
    current_timestamp = int(time.time())
    assert (
        token["expires_at"]
        == current_timestamp + get_settings().security.jwt_access_token_expire_secs
    )


@freeze_time("2023-01-01")
async def test_refresh_token_success_jwt_has_valid_access_token(
    client: AsyncClient,
    default_user: User,
    session: AsyncSession,
) -> None:
    test_refresh_token = RefreshToken(
        user_id=default_user.user_id,
        refresh_token="blaxx",
        exp=int(time.time()) + 1000,
        used=False,
    )
    session.add(test_refresh_token)
    await session.commit()

    response = await client.post(
        app.url_path_for("refresh_token"),
        json={
            "refresh_token": "blaxx",
        },
    )

    now = int(time.time())
    token = response.json()
    token_payload = verify_jwt_token(token["access_token"])

    assert token_payload.sub == default_user.user_id
    assert token_payload.iat == now
    assert token_payload.exp == token["expires_at"]


@freeze_time("2023-01-01")
async def test_refresh_token_success_refresh_token_has_valid_expire_time(
    client: AsyncClient,
    default_user: User,
    session: AsyncSession,
) -> None:
    test_refresh_token = RefreshToken(
        user_id=default_user.user_id,
        refresh_token="blaxx",
        exp=int(time.time()) + 1000,
        used=False,
    )
    session.add(test_refresh_token)
    await session.commit()

    response = await client.post(
        app.url_path_for("refresh_token"),
        json={
            "refresh_token": "blaxx",
        },
    )

    token = response.json()
    current_time = int(time.time())
    assert (
        token["refresh_token_expires_at"]
        == current_time + get_settings().security.refresh_token_expire_secs
    )


async def test_refresh_token_success_new_refresh_token_is_in_db(
    client: AsyncClient,
    default_user: User,
    session: AsyncSession,
) -> None:
    test_refresh_token = RefreshToken(
        user_id=default_user.user_id,
        refresh_token="blaxx",
        exp=int(time.time()) + 1000,
        used=False,
    )
    session.add(test_refresh_token)
    await session.commit()

    response = await client.post(
        app.url_path_for("refresh_token"),
        json={
            "refresh_token": "blaxx",
        },
    )

    token = response.json()
    token_db_count = await session.scalar(
        select(func.count()).where(RefreshToken.refresh_token == token["refresh_token"])
    )
    assert token_db_count == 1
