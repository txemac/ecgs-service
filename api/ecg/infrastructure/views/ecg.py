import logging
from uuid import uuid4

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pydantic.types import UUID4
from sqlalchemy.orm import Session
from starlette import status

from api import messages
from api.database import db_sql_session
from api.depends import get_channel_repository
from api.depends import get_ecg_repository
from api.ecg.application.calculate_zero_crossing import calculate_zero_crossing
from api.ecg.domain.channel_repository import ChannelRepository
from api.ecg.domain.ecg import Channel
from api.ecg.domain.ecg import ECG
from api.ecg.domain.ecg import ECGID
from api.ecg.domain.ecg import ECGIn
from api.ecg.domain.ecg import ECGOutWithChannels
from api.ecg.domain.ecg_repository import ECGRepository

logger = logging.getLogger(__name__)

ecgs_router = APIRouter()


@ecgs_router.post(
    path="",
    name="Create ECG",
    description="Create a new ECG.",
    status_code=status.HTTP_201_CREATED,
    response_model=ECGID,
)
def create_ecg(
        payload: ECGIn,
        db_sql: Session = Depends(db_sql_session),
        ecg_repository: ECGRepository = Depends(get_ecg_repository),
        channel_repository: ChannelRepository = Depends(get_channel_repository),
) -> ECGID:
    logger.info(f"POST Company. Payload: {payload.dict()}")

    new_ecg = ECG(
        id=uuid4(),
        date=payload.date,
    )
    ecg = ecg_repository.create(db_sql, new_ecg=new_ecg)

    for channel in payload.channels:
        new_channel = Channel(
            ecg_id=ecg.id,
            name=channel.name,
            num_zero_crossing=calculate_zero_crossing(signal=channel.signal),
        )
        channel_repository.create(db_sql, new_channel=new_channel)

    return ECGID(id=ecg.id)


@ecgs_router.get(
    path="/{ecg_id}",
    name="Get one",
    description="Get user info.",
    status_code=status.HTTP_200_OK,
    response_model=ECGOutWithChannels,
    responses={
        404: {"description": messages.ECG_NOT_FOUND},
    },
)
def get_one(
        ecg_id: UUID4,
        db_sql: Session = Depends(db_sql_session),
        ecg_repository: ECGRepository = Depends(get_ecg_repository),
) -> ECGOutWithChannels:
    logger.info(f"GET ECG. ecg_id: {ecg_id}")

    ecg = ecg_repository.get_by_id(db_sql, ecg_id=ecg_id)
    if not ecg:
        logger.exception(f"{messages.ECG_NOT_FOUND} - ID: {ecg_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.ECG_NOT_FOUND)

    return ecg
