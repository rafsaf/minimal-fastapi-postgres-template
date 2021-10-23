from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.core.security import get_password_hash

router = APIRouter()


@router.put("/me", response_model=schemas.User)
def update_user_me(
    user_update: schemas.UserUpdate,
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update me.
    """
    if user_update.password is not None:
        current_user.hashed_password = get_password_hash(user_update.password)
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.email is not None:
        current_user.email = user_update.email

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
