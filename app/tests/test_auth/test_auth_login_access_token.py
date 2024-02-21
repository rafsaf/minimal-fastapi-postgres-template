from datetime import UTC, datetime

from fastapi import status
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security.jwt import verify_jwt_token
from app.main import app
from app.models import RefreshToken, User
from app.tests.conftest import default_user_password
from freezegun import freeze_time


@freeze_time("2023-01-01")
async def test_login_access_token_has_response_code_200(
    client: AsyncClient,
    default_user: User,
) -> None:
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": default_user.email,
            "password": default_user_password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_200_OK


@freeze_time("2023-01-01")
async def test_login_access_token_jwt_has_valid_token_type(
    client: AsyncClient,
    default_user: User,
) -> None:
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": default_user.email,
            "password": default_user_password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token = response.json()
    assert token["token_type"] == "Bearer"


@freeze_time("2023-01-01")
async def test_login_access_token_jwt_has_valid_expire_time(
    client: AsyncClient,
    default_user: User,
) -> None:
    current_time = int(datetime.now(tz=UTC).timestamp())
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": default_user.email,
            "password": default_user_password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token = response.json()
    assert (
        current_time + get_settings().security.jwt_access_token_expire_secs
        <= token["expires_at"]
        <= current_time + get_settings().security.jwt_access_token_expire_secs + 1
    )


async def test_login_access_token_returns_valid_jwt_access_token(
    client: AsyncClient,
    default_user: User,
) -> None:
    now = int(datetime.now(tz=UTC).timestamp())
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": default_user.email,
            "password": default_user_password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token = response.json()
    token_payload = verify_jwt_token(token["access_token"])

    assert token_payload.sub == default_user.user_id
    assert token_payload.iat >= now
    assert token_payload.exp == token["expires_at"]


async def test_login_access_token_refresh_token_has_valid_expire_time(
    client: AsyncClient,
    default_user: User,
) -> None:
    current_time = int(datetime.now(tz=UTC).timestamp())
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": default_user.email,
            "password": default_user_password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token = response.json()
    assert (
        current_time + get_settings().security.refresh_token_expire_secs
        <= token["refresh_token_expires_at"]
        <= current_time + get_settings().security.refresh_token_expire_secs + 1
    )


async def test_login_access_token_refresh_token_exists_in_db(
    client: AsyncClient,
    default_user: User,
    session: AsyncSession,
) -> None:
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": default_user.email,
            "password": default_user_password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token = response.json()

    token_db_count = await session.scalar(
        select(func.count()).where(RefreshToken.refresh_token == token["refresh_token"])
    )
    assert token_db_count == 1


async def test_login_access_token_refresh_token_in_db_has_valid_fields(
    client: AsyncClient,
    default_user: User,
    session: AsyncSession,
) -> None:
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": default_user.email,
            "password": default_user_password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token = response.json()
    result = await session.scalars(
        select(RefreshToken).where(RefreshToken.refresh_token == token["refresh_token"])
    )
    refresh_token = result.one()

    assert refresh_token.user_id == default_user.user_id
    assert refresh_token.exp == token["refresh_token_expires_at"]
    assert not refresh_token.used


async def test_auth_access_token_fail_for_not_existing_user(
    client: AsyncClient,
) -> None:
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": "non-existing",
            "password": "bla",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}


async def test_auth_access_token_fail_for_invalid_password(
    client: AsyncClient,
    default_user: User,
) -> None:
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": default_user.email,
            "password": "invalid",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}
