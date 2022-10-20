import logging
from typing import Any
from typing import Dict
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

from api.ecg.domain.channel_repository import ChannelRepository
from api.ecg.domain.ecg import Channel
from api.ecg.domain.ecg import ECG
from api.ecg.domain.ecg_repository import ECGRepository
from api.ecg.infrastructure.repositories.sqlmodel_channel_repository import SQLModelChannelRepository
from api.ecg.infrastructure.repositories.sqlmodel_ecg_repository import SQLModelECGRepository
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


@pytest.fixture
def ecg_repository() -> ECGRepository:
    return SQLModelECGRepository()


@pytest.fixture
def channel_repository() -> ChannelRepository:
    return SQLModelChannelRepository()


@pytest.fixture
def new_ecg_data() -> Dict:
    return dict(
        date="2022-03-07 02:54:04",
    )


@pytest.fixture
def ecg_1(
        db_sql: Session,
        ecg_repository: ECGRepository,
        new_ecg_data: Dict,
) -> ECG:
    return ecg_repository.create(db_sql, new_ecg=ECG(**new_ecg_data))


@pytest.fixture
def new_channel_data(
        ecg_1: ECG,
) -> Dict:
    return dict(
        ecg_id=ecg_1.id,
        name="II",
        num_zero_crossing=17,
    )


@pytest.fixture
def channel_1(
        db_sql: Session,
        channel_repository: ChannelRepository,
        new_channel_data: Dict,
) -> Channel:
    return channel_repository.create(db_sql, new_channel=Channel(**new_channel_data))
