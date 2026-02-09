import logging
from typing import TypeVar

from faker import Faker
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from polyfactory.fields import Use

from app.auth.models import User
from app.auth.password import get_password_hash
from app.tests.auth import TESTS_USER_PASSWORD

logging.getLogger("factory").setLevel(logging.ERROR)


T = TypeVar("T")


logger = logging.getLogger(__name__)


class UserFactory(SQLAlchemyFactory[User]):
    email = Use(Faker().email)
    hashed_password = Use(lambda: get_password_hash(TESTS_USER_PASSWORD))
