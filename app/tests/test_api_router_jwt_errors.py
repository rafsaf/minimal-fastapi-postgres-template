import pytest
from fastapi import routing, status
from freezegun import freeze_time
from httpx import AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import api_messages
from app.api.api_router import api_router
from app.core.security.jwt import create_jwt_token
from app.models import User


@pytest.mark.parametrize("api_route", api_router.routes)
async def test_api_routes_raise_401_on_jwt_decode_errors(
    client: AsyncClient,
    api_route: routing.APIRoute,
) -> None:
    for method in api_route.methods:
        response = await client.request(
            method=method,
            url=api_route.path,
            headers={"Authorization": "Bearer garbage-invalid-jwt"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Token invalid: Not enough segments"}


@pytest.mark.parametrize("api_route", api_router.routes)
async def test_api_routes_raise_401_on_jwt_expired_token(
    client: AsyncClient,
    default_user: User,
    api_route: routing.APIRoute,
) -> None:
    with freeze_time("2023-01-01"):
        jwt = create_jwt_token(default_user.user_id)
    with freeze_time("2023-02-01"):
        for method in api_route.methods:
            response = await client.request(
                method=method,
                url=api_route.path,
                headers={"Authorization": f"Bearer {jwt.access_token}"},
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
            assert response.json() == {"detail": "Token invalid: Signature has expired"}


@pytest.mark.parametrize("api_route", api_router.routes)
async def test_api_routes_raise_401_on_jwt_user_deleted(
    client: AsyncClient,
    default_user_headers: dict[str, str],
    default_user: User,
    api_route: routing.APIRoute,
    session: AsyncSession,
) -> None:
    await session.execute(delete(User).where(User.user_id == default_user.user_id))
    await session.commit()

    for method in api_route.methods:
        response = await client.request(
            method=method,
            url=api_route.path,
            headers=default_user_headers,
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": api_messages.JWT_ERROR_USER_REMOVED}
