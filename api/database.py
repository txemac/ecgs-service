from sqlmodel import MetaData
from sqlmodel import Session
from sqlmodel import create_engine
from sqlmodel.sql.expression import Select
from sqlmodel.sql.expression import SelectOfScalar

from api.settings import DATABASE_URL

# TODO: these should not have to be set
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
metadata = MetaData(naming_convention=NAMING_CONVENTION)


def db_sql_session() -> Session:
    with Session(engine, autoflush=True) as session:
        yield session
