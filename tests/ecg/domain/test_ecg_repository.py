from typing import Dict
from uuid import uuid4

from pydantic import UUID4
from sqlmodel import Session

from api.ecg.domain.ecg import ECG
from api.ecg.domain.ecg_repository import ECGRepository
from tests.utils import assert_dicts


def test_count_0(
        db_sql: Session,
        ecg_repository: ECGRepository,
) -> None:
    assert ecg_repository.count(db_sql) == 0


def test_count_1(
        db_sql: Session,
        ecg_repository: ECGRepository,
        ecg_1: ECG,
) -> None:
    assert ecg_repository.count(db_sql) == 1


def test_create_ok(
        db_sql: Session,
        ecg_repository: ECGRepository,
        new_ecg_data: Dict,
) -> None:
    count_1 = ecg_repository.count(db_sql)
    new_ecg = ECG(
        id=uuid4(),
        date=new_ecg_data["date"]
    )
    ecg = ecg_repository.create(db_sql, new_ecg=new_ecg)
    count_2 = ecg_repository.count(db_sql)

    assert count_1 + 1 == count_2

    assert ecg_repository.get_by_id(db_sql, ecg_id=ecg.id) == ecg


def test_get_by_id_ok(
        db_sql: Session,
        ecg_repository: ECGRepository,
        ecg_1: ECG,
) -> None:
    result = ecg_repository.get_by_id(db_sql, ecg_id=ecg_1.id)
    assert_dicts(original=result.dict(), expected=ecg_1.dict())


def test_get_by_id_not_exists(
        db_sql: Session,
        ecg_repository: ECGRepository,
) -> None:
    assert ecg_repository.get_by_id(db_sql, ecg_id=UUID4(str(uuid4()))) is None
