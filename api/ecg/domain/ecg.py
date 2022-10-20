from datetime import datetime
from typing import List
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel
from pydantic.types import UUID4
from pydantic.types import conint
from pydantic.types import conlist
from pydantic.types import constr
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel
from sqlmodel import UniqueConstraint


class ChannelIn(BaseModel):
    name: constr(min_length=1)
    num_samples: Optional[conint(gt=1)]
    signal: conlist(item_type=int, min_items=1)


class ECGIn(BaseModel):
    date: datetime
    channels: conlist(item_type=ChannelIn, min_items=1)

    class Config:
        schema_extra = dict(
            example=dict(
                date="2022-03-07 02:54:04",
                channels=[
                    dict(
                        name="I",
                        num_samples=10,
                        signal=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    ),
                ],
            ),
        )


class Channel(SQLModel, table=True):
    __tablename__ = "channel"

    __table_args__ = (
        UniqueConstraint('ecg_id', 'name', name='ck_channel_ecg_id_name'),
    )

    ecg_id: UUID4 = Field(foreign_key="ecg.id", nullable=False, primary_key=True)
    ecg: "ECG" = Relationship()  # noqa: F821
    name: constr(min_length=1) = Field(primary_key=True, nullable=False)
    num_zero_crossing: conint(ge=0)


class ECG(SQLModel, table=True):
    __tablename__ = "ecg"

    id: UUID4 = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = datetime.utcnow()
    date: datetime

    channels: List[Channel] = Relationship(back_populates="ecg")


class ECGID(BaseModel):
    id: UUID4
