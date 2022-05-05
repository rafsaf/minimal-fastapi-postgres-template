"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head
"""

import uuid
from dataclasses import dataclass, field

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

Base = registry()


def random_uuid():
    return str(uuid.uuid4())


@Base.mapped
@dataclass
class User:
    __tablename__ = "user"
    __sa_dataclass_metadata_key__ = "sa"

    id: str = field(
        init=False,
        default_factory=random_uuid,
        metadata={
            "sa": Column(UUID(as_uuid=False), primary_key=True, default=random_uuid)
        },
    )
    email: str = field(metadata={"sa": Column(String(254), nullable=False, index=True)})
    hashed_password: str = field(metadata={"sa": Column(String(128), nullable=False)})
    full_name: str | None = field(
        default=None, metadata={"sa": Column(String(254), nullable=True)}
    )
