"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

Note, it is used by alembic migrations logic, see `alembic/env.py`

"""

from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import registry

Base = registry()


@Base.mapped
@dataclass
class User:
    __tablename__ = "user"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    email: str = field(metadata={"sa": Column(String(254), nullable=False, index=True)})
    hashed_password: str = field(metadata={"sa": Column(String(128), nullable=False)})
    full_name: str | None = field(
        default=None, metadata={"sa": Column(String(254), nullable=True)}
    )
