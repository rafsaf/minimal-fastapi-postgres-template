import logging
from typing import TypeVar

from faker import Faker
from polyfactory.factories.sqlalchemy_factory import (
    SQLAASyncPersistence,
    SQLAlchemyFactory,
)
from polyfactory.fields import Use

from app.auth.models import User
from app.tests.auth import TESTS_USER_PASSWORD_HASH

logging.getLogger("factory").setLevel(logging.ERROR)


T = TypeVar("T")


logger = logging.getLogger(__name__)


class SQLAlchemySessionMixin[T]:
    __async_persistence__: SQLAASyncPersistence[T] | None = None


class UserFactory(SQLAlchemySessionMixin[User], SQLAlchemyFactory[User]):
    email = Use(Faker().email)
    hashed_password = TESTS_USER_PASSWORD_HASH
