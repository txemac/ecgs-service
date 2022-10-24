from abc import ABC
from abc import abstractmethod
from typing import Optional

from pydantic import UUID4
from sqlmodel import Session

from api.ecg.domain.ecg import ECG
from api.ecg.domain.ecg import ECGOutWithChannels


class ECGRepository(ABC):

    @staticmethod
    @abstractmethod
    def count(
            db_sql: Session,
    ) -> int:
        """
        Count the number of element in the ECG table.

        :param db_sql: session of the SQL database
        :return: number of ECGs
        """
        pass

    @staticmethod
    @abstractmethod
    def create(
            db_sql: Session,
            new_ecg: ECG,
    ) -> Optional[ECG]:
        """
        Persist a new ECG.

        :param db_sql: session of the SQL database
        :param new_ecg: new ECG to persist
        :return: ECG if the record was created, None otherwise
        """
        pass

    @staticmethod
    @abstractmethod
    def get_by_id(
            db_sql: Session,
            ecg_id: UUID4,
    ) -> Optional[ECGOutWithChannels]:
        """
        Searches for a persisted ECG by ID and returns it if it exists.

        :param db_sql: session of the SQL database
        :param ecg_id: ID of the ECG
        :return: info about ECG if found, None otherwise
        """
        pass
