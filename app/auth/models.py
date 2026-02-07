# SQL Alchemy models declaration.
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models
# mapped_column syntax from SQLAlchemy 2.0.

# https://alembic.sqlalchemy.org/en/latest/tutorial.html
# Note, it is used by alembic migrations logic, see `alembic/env.py`

# Alembic shortcuts:
# # create migration
# alembic revision --autogenerate -m "migration_name"

# # apply all migrations
# alembic upgrade head


import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models import Base


class User(Base):
    __tablename__ = "auth_user"

    user_id: Mapped[str] = mapped_column(
        sa.String(36), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(
        sa.String(256), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(sa.String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user")  # noqa: UP037


class RefreshToken(Base):
    __tablename__ = "auth_refresh_token"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    refresh_token: Mapped[str] = mapped_column(
        sa.String(512), nullable=False, unique=True, index=True
    )
    used: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=False)
    exp: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)

    user_id: Mapped[str] = mapped_column(
        sa.ForeignKey("auth_user.user_id", ondelete="CASCADE"),
    )
    user: Mapped[User] = relationship(back_populates="refresh_tokens")
