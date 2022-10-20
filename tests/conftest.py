from copy import deepcopy
from typing import Dict

import pytest as pytest

from src.ecg.domain.ecg import ECGIn


@pytest.fixture
def new_ecg_in_data() -> Dict:
    return deepcopy(ECGIn.Config.schema_extra.get("example"))


@pytest.fixture
def new_channel_in_data(
        new_ecg_in_data: Dict,
) -> Dict:
    return new_ecg_in_data["channels"][0]


@pytest.fixture
def new_channel_out_data() -> Dict:
    return dict(
        name="II",
        num_zero_crossing=17,
    )


@pytest.fixture
def new_ecg_out_data(
        new_channel_out_data: Dict,
) -> Dict:
    return dict(
        id="463b94cb-71e6-4fcb-bd52-d1b3288a2232",
        created_at="2022-03-09 01:23:45",
        date="2022-03-07 02:54:04",
        channels=[new_channel_out_data],
    )
