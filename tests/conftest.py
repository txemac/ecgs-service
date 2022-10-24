import logging
from typing import Any
from typing import Dict
from typing import Generator

import pytest
from alembic.command import downgrade
from alembic.command import upgrade
from alembic.config import Config
from pydantic.networks import EmailStr
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from sqlmodel import Session
from sqlmodel import create_engine
from starlette.config import environ
from starlette.testclient import TestClient

from api.database import db_sql_session
from api.ecg.domain.channel_repository import ChannelRepository
from api.ecg.domain.ecg import ECG
from api.ecg.domain.ecg_repository import ECGRepository
from api.ecg.infrastructure.repositories.sqlmodel_channel_repository import SQLModelChannelRepository
from api.ecg.infrastructure.repositories.sqlmodel_ecg_repository import SQLModelECGRepository
from api.main import api
from api.settings import DATABASE_URL
from api.user.application.create_access_token import create_access_token
from api.user.application.password_hash import get_password_hash
from api.user.domain.user import RoleEnum
from api.user.domain.user import User
from api.user.domain.user import UserCreate
from api.user.domain.user_repository import UserRepository
from api.user.infrastructure.repositories.sqlmodel_user_repository import SQLModelUserRepository

environ["TESTING"] = "True"
logging.getLogger("alembic").setLevel(logging.ERROR)


@pytest.fixture
def client(
        db_sql: Session,
) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        try:
            yield db_sql
        finally:
            pass

    api.dependency_overrides[db_sql_session] = _get_test_db
    with TestClient(api) as client:
        yield client


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
def user_repository() -> UserRepository:
    return SQLModelUserRepository()


@pytest.fixture
def new_ecg_data() -> Dict:
    return dict(
        date="2022-10-20 17:25:00",
        channels=[
            dict(
                name="I",
                num_samples=10,
                signal=[1, -2, 3, -4, 5, -6, 7, -8, 9, -10],
            ),
        ],
    )


@pytest.fixture
def ecg_1(
        client: TestClient,
        db_sql: Session,
        new_ecg_data: Dict,
) -> ECG:
    response = client.post(
        url="/ecgs",
        json=new_ecg_data,
    )
    return ECG(**response.json())


@pytest.fixture
def new_user_data() -> Dict:
    return dict(
        email=EmailStr("email@gmail.com"),
        password="12345678",
        role=RoleEnum.USER,
    )


@pytest.fixture
def new_user(
        db_sql: Session,
        user_repository: UserRepository,
        new_user_data: Dict,
):
    def _new_user(
            email: str,
            role: RoleEnum = RoleEnum.USER,
    ) -> User:
        user_data = UserCreate(**new_user_data)
        user_data.email = email
        user_data.role = role
        user_data.password = get_password_hash(user_data.password)
        user = user_repository.create(db_sql, new_user=user_data)
        return user

    yield _new_user


@pytest.fixture
def user_admin(
        new_user,
) -> User:
    return new_user(email="admin@gmail.com", role=RoleEnum.ADMIN)


@pytest.fixture
def user_1(
        new_user,
) -> User:
    return new_user(email="user_1@gmail.com")


@pytest.fixture
def headers_user_admin(
        user_admin: User,
) -> Dict[str, str]:
    return dict(Authorization=f"Bearer {create_access_token(email=user_admin.email)}")


@pytest.fixture
def headers_user_1(
        user_1: User,
) -> Dict[str, str]:
    return dict(Authorization=f"Bearer {create_access_token(email=user_1.email)}")
