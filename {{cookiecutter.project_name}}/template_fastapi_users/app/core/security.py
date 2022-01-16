"""
You can have several authentication methods, e.g. a cookie 
authentication for browser-based queries and a JWT token authentication for pure API queries.

In this template, token will be sent through Bearer header
{"Authorization": "Bearer xyz"}
using JWT tokens.

There are more option to consider, refer to
https://fastapi-users.github.io/fastapi-users/configuration/authentication/ 

UserManager class is core fastapi users class with customizable attrs and methods
https://fastapi-users.github.io/fastapi-users/configuration/user-manager/
"""


from typing import Optional

from fastapi import Request
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.manager import BaseUserManager

from app import schemas
from app.core import config


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=config.settings.SECRET_KEY,
        lifetime_seconds=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


BEARER_TRANSPORT = BearerTransport(tokenUrl="auth/jwt/login")
AUTH_BACKEND = AuthenticationBackend(
    name="jwt",
    transport=BEARER_TRANSPORT,
    get_strategy=get_jwt_strategy,
)


class UserManager(BaseUserManager[schemas.UserCreate, schemas.UserDB]):
    user_db_model = schemas.UserDB
    reset_password_token_secret = config.settings.SECRET_KEY
    verification_token_secret = config.settings.SECRET_KEY

    async def on_after_register(
        self, user: schemas.UserDB, request: Optional[Request] = None
    ):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: schemas.UserDB, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: schemas.UserDB, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
