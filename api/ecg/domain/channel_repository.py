from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional

from pydantic import UUID4
from sqlmodel import Session

from api.ecg.domain.ecg import Channel


class ChannelRepository(ABC):

    @staticmethod
    @abstractmethod
    def count(
            db_sql: Session,
    ) -> int:
        """
        Count the number of element in the channel table.

        :param db_sql: session of the SQL database
        :return: number of channels
        """
        pass

    @staticmethod
    @abstractmethod
    def create(
            db_sql: Session,
            new_channel: Channel,
    ) -> Optional[Channel]:
        """
        Persist a new Channel.

        :param db_sql: session of the SQL database
        :param new_channel: new Channel to persist
        :return: Channel if the record was created, None otherwise
        """
        pass

    @staticmethod
    @abstractmethod
    def get_list_by_ecg_id(
            db_sql: Session,
            ecg_id: UUID4,
    ) -> List[Channel]:
        """
        Searches for a persisted channels by ID of the ECG and returns them if they exist.

        :param db_sql: session of the SQL database
        :param ecg_id: ID of the ECG
        :return: info about channels if found, None otherwise
        """
        pass
