from typing import Any, cast

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = cast(Any, declarative_base())


class User(Base):
    __tablename__ = "user"
    id = cast(int, Column(Integer, primary_key=True, index=True))
    full_name = cast(str, Column(String(254), nullable=True))
    email = cast(str, Column(String(254), unique=True, index=True, nullable=False))
    hashed_password = cast(str, Column(String(128), nullable=False))
