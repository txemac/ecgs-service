from abc import ABC
from abc import abstractmethod
from typing import Optional

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
