from typing import Dict

from sqlmodel import Session

from api.ecg.domain.channel_repository import ChannelRepository
from api.ecg.domain.ecg import Channel


def test_count_0(
        db_sql: Session,
        channel_repository: ChannelRepository,
) -> None:
    assert channel_repository.count(db_sql) == 0


def test_count_1(
        db_sql: Session,
        channel_repository: ChannelRepository,
        channel_1: Channel,
) -> None:
    assert channel_repository.count(db_sql) == 1


def test_create_ok(
        db_sql: Session,
        channel_repository: ChannelRepository,
        new_channel_data: Dict,
) -> None:
    count_1 = channel_repository.count(db_sql)
    channel_repository.create(db_sql, new_channel=Channel(**new_channel_data))
    count_2 = channel_repository.count(db_sql)

    assert count_1 + 1 == count_2
