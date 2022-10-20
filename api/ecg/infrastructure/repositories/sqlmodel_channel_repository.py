import logging

from sqlmodel import Session

from api.ecg.domain.channel_repository import ChannelRepository
from api.ecg.domain.ecg import Channel

logger = logging.getLogger(__name__)


class SQLModelChannelRepository(ChannelRepository):

    @staticmethod
    def count(
            db_sql: Session,
    ) -> int:
        result = db_sql.query(Channel).count()
        logger.info(f"SQL query count to Channel with result {result}")
        return result

    @staticmethod
    def create(
            db_sql: Session,
            new_channel: Channel,
    ) -> Channel:
        channel = Channel.from_orm(new_channel)
        db_sql.add(channel)
        db_sql.commit()
        db_sql.refresh(channel)
        logger.info(f"SQL query add new Channel to ECG with ID {channel.ecg_id}")
        return channel
