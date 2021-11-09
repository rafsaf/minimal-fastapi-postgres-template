import pytest
from httpx import AsyncClient

from app.models import User

# All test coroutines in file will be treated as marked (async allowed).
pytestmark = pytest.mark.asyncio


async def test_login_endpoints(client: AsyncClient, default_user: User):

    # access-token endpoint
    access_token = await client.post(
        "/auth/access-token",
        data={
            "username": "user@email.com",
            "password": "password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert access_token.status_code == 200
    token = access_token.json()

    access_token = token["access_token"]
    refresh_token = token["refresh_token"]

    # test-token endpoint
    test_token = await client.post(
        "/auth/test-token", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert test_token.status_code == 200
    response_user = test_token.json()
    assert response_user["email"] == default_user.email

    # refresh-token endpoint
    get_new_token = await client.post(
        "/auth/refresh-token", json={"refresh_token": refresh_token}
    )

    assert get_new_token.status_code == 200
    new_token = get_new_token.json()

    assert "access_token" in new_token
