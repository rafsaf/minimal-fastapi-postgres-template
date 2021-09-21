from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from jose import jwt
from pydantic import ValidationError

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token, expire_at = security.create_access_token(user.id)
    refresh_token, refresh_expire_at = security.create_refresh_token(user.id)
    return {
        "token_type": "bearer",
        "access_token": access_token,
        "expire_at": expire_at,
        "refresh_token": refresh_token,
        "refresh_expire_at": refresh_expire_at,
    }


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/refresh-token", response_model=schemas.Token)
async def refresh_token(refresh_token: str, db: Session = Depends(deps.get_db)):
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    if not token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    access_token, expire_at = security.create_access_token(user.id)
    refresh_token, refresh_expire_at = security.create_refresh_token(user.id)
    return {
        "token_type": "bearer",
        "access_token": access_token,
        "expire_at": expire_at,
        "refresh_token": refresh_token,
        "refresh_expire_at": refresh_expire_at,
    }
