import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.api import deps
from app.core import config, security
from app.models import User

router = APIRouter()


@router.post("/access-token", response_model=schemas.Token, name="access_token")
async def login_access_token(
    session: AsyncSession = Depends(deps.get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 compatible token, get an access token for future requests using username and password
    """
    # https://www.oauth.com/oauth2-servers/access-tokens/access-token-response/

    result = await session.execute(select(User).where(User.email == form_data.username))
    user: User | None = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return security.access_token_response(user.id)


@router.post("/refresh-token", response_model=schemas.Token, name="refresh_token")
async def refresh_token(
    input: schemas.TokenRefresh, session: AsyncSession = Depends(deps.get_session)
):
    """
    OAuth2 compatible token, get an access token for future requests using refresh token
    """
    try:
        payload = jwt.decode(
            input.refresh_token,
            config.settings.SECRET_KEY,
            algorithms=[security.JWT_ALGORITHM],
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.DecodeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    if not token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    result = await session.execute(select(User).where(User.id == token_data.sub))
    user: User | None = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return security.access_token_response(user.id)
