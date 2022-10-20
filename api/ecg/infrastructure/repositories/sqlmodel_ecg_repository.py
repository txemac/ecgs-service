import logging
from typing import Optional

from pydantic import UUID4
from sqlmodel import Session

from api.ecg.domain.ecg import ECG
from api.ecg.domain.ecg_repository import ECGRepository

logger = logging.getLogger(__name__)


class SQLModelECGRepository(ECGRepository):

    @staticmethod
    def count(
            db_sql: Session,
    ) -> int:
        result = db_sql.query(ECG).count()
        logger.info(f"SQL query count to ECG with result {result}")
        return result

    @staticmethod
    def create(
            db_sql: Session,
            new_ecg: ECG,
    ) -> ECG:
        ecg = ECG.from_orm(new_ecg)
        db_sql.add(ecg)
        db_sql.commit()
        db_sql.refresh(ecg)
        logger.info(f"SQL query add new ECG with ID {ecg.id}")
        return ecg

    @staticmethod
    def get_by_id(
            db_sql: Session,
            ecg_id: UUID4,
    ) -> Optional[ECG]:
        logger.info(f"SQL query get ECG with ID {ecg_id}")
        return db_sql.get(ECG, ecg_id)
