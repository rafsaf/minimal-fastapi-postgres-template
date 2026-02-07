from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import api_messages
from app.auth.jwt import verify_jwt_token
from app.auth.models import User
from app.core import database_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/access-token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(database_session.new_async_session),
) -> User:
    token_payload = verify_jwt_token(token)

    user = await session.scalar(select(User).where(User.user_id == token_payload.sub))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=api_messages.JWT_ERROR_USER_REMOVED,
        )
    return user
