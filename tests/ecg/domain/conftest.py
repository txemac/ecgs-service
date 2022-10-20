import logging
from typing import Any
from typing import Generator

import pytest
from alembic.command import downgrade
from alembic.command import upgrade
from alembic.config import Config
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from sqlmodel import Session
from sqlmodel import create_engine
from starlette.config import environ

from api.settings import DATABASE_URL

environ["TESTING"] = "True"
logging.getLogger("alembic").setLevel(logging.ERROR)


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    return engine


@pytest.fixture(scope="session")
def db_migrations(db_engine) -> None:
    config = Config("alembic.ini")
    upgrade(config, "head")
    yield
    downgrade(config, "base")


@pytest.fixture
def db_sql(db_engine, db_migrations) -> Generator[Session, Any, None]:
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
