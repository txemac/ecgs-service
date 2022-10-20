from sqlmodel import Session

from api.ecg.domain.channel_repository import ChannelRepository
from api.ecg.domain.ecg import Channel
from api.ecg.domain.ecg import ECG


def test_count_0(
        db_sql: Session,
        channel_repository: ChannelRepository,
) -> None:
    assert channel_repository.count(db_sql) == 0


def test_count_1(
        db_sql: Session,
        channel_repository: ChannelRepository,
        ecg_1: ECG,
) -> None:
    assert channel_repository.count(db_sql) == 1


def test_create_ok(
        db_sql: Session,
        channel_repository: ChannelRepository,
        ecg_1: ECG,
) -> None:
    count_1 = channel_repository.count(db_sql)
    new_channel = Channel(
        ecg_id=ecg_1.id,
        name="II",
        num_zero_crossing=17,
    )
    channel_repository.create(db_sql, new_channel=new_channel)
    count_2 = channel_repository.count(db_sql)

    assert count_1 + 1 == count_2
