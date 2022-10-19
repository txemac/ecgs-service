from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.types import conint
from pydantic.types import conlist
from pydantic.types import constr


class Channel(BaseModel):
    name: constr(min_length=1)
    num_samples: Optional[conint(gt=1)]
    signal: conlist(item_type=int, min_items=1)


class ECG(BaseModel):
    date: datetime
    channels: conlist(item_type=Channel, min_items=1)

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
