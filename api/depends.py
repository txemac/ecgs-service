from api.ecg.domain.channel_repository import ChannelRepository
from api.ecg.domain.ecg_repository import ECGRepository
from api.ecg.infrastructure.repositories.sqlmodel_channel_repository import SQLModelChannelRepository
from api.ecg.infrastructure.repositories.sqlmodel_ecg_repository import SQLModelECGRepository


def get_ecg_repository() -> ECGRepository:
    return SQLModelECGRepository()


def get_channel_repository() -> ChannelRepository:
    return SQLModelChannelRepository()
