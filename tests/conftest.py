from copy import deepcopy
from typing import Dict

import pytest as pytest

from src.ecg.domain.ecg import ECG


@pytest.fixture
def new_ecg_data() -> Dict:
    return deepcopy(ECG.Config.schema_extra.get("example"))


@pytest.fixture
def new_channel_data(
        new_ecg_data: Dict,
) -> Dict:
    return new_ecg_data["channels"][0]
