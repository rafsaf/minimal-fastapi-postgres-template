from datetime import datetime, timezone
from httpx import AsyncClient

from fastapi import status
from sqlalchemy import select
from app.main import app
from app.models import RefreshToken, User
from app.core.config import get_settings
from app.core.security.jwt import verify_jwt_token
from app.tests.conftest import default_user_email, default_user_password
from freezegun import freeze_time
from sqlalchemy.ext.asyncio import AsyncSession


async def test_login_access_token_return_success_response(
    client: AsyncClient, default_user: User
) -> None:
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": default_user_email,
            "password": default_user_password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_200_OK

    token = response.json()
    assert token["token_type"] == "Bearer"


@freeze_time("2024-01-19")
async def test_login_access_token_return_valid_jwt_access_token(
    client: AsyncClient, default_user: User
) -> None:
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": default_user_email,
            "password": default_user_password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token = response.json()
    expected_exp = int(
        datetime.now(tz=timezone.utc).timestamp()
        + get_settings().security.jwt_access_token_expire_secs
    )
    assert token["expires_in"] == expected_exp
    token_payload = verify_jwt_token(token["access_token"])
    assert token_payload.sub == default_user.user_id
    assert token_payload.iat == int(datetime.now(tz=timezone.utc).timestamp())
    assert token_payload.exp == expected_exp


@freeze_time("2024-01-19")
async def test_login_access_token_return_valid_refresh_token(
    client: AsyncClient, default_user: User, session: AsyncSession
) -> None:
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": default_user_email,
            "password": default_user_password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token = response.json()
    expected_exp = int(
        datetime.now(tz=timezone.utc).timestamp()
        + get_settings().security.refresh_token_expire_secs
    )
    assert token["refresh_token_expires_in"] == expected_exp
    result = await session.execute(
        select(RefreshToken).where(RefreshToken.refresh_token == token["refresh_token"])
    )
    refresh_token = result.scalars().first()
    assert refresh_token is not None
    assert refresh_token.user_id == default_user.user_id
    assert refresh_token.exp == expected_exp
    assert not refresh_token.used


async def test_auth_access_token_fail_no_user(client: AsyncClient) -> None:
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": "xxx",
            "password": "yyy",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Incorrect email or password"}


async def test_auth_refresh_token(client: AsyncClient, default_user: User) -> None:
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": default_user_email,
            "password": default_user_password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    refresh_token = response.json()["refresh_token"]

    new_token_response = await client.post(
        app.url_path_for("refresh_token"), json={"refresh_token": refresh_token}
    )
    assert new_token_response.status_code == status.HTTP_200_OK
    token = new_token_response.json()
    assert token["token_type"] == "Bearer"
    assert "access_token" in token
    assert "expires_at" in token
    assert "issued_at" in token
    assert "refresh_token" in token
    assert "refresh_token_expires_at" in token
    assert "refresh_token_issued_at" in token
