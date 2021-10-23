from typing import Optional

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models import User

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


@pytest.fixture
async def default_user(session: AsyncSession):
    result = await session.execute(select(User).where(User.email == "user@email.com"))
    user: Optional[User] = result.scalars().first()
    if user is None:
        new_user = User(
            email="user@email.com",
            hashed_password=get_password_hash("password"),
            full_name="fullname",
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    return user


async def test_login_endpoints(client: AsyncClient, default_user: User):

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

    test_token = await client.post(
        "/auth/test-token", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert test_token.status_code == 200
    response_user = test_token.json()
    assert response_user["email"] == default_user.email

    get_new_token = await client.post(
        "/auth/refresh-token", json={"refresh_token": refresh_token}
    )

    assert get_new_token.status_code == 200
    new_token = get_new_token.json()

    assert "access_token" in new_token
