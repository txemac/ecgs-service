from copy import deepcopy
from typing import Dict

import pytest

from api.ecg.domain.ecg import ECGIn


@pytest.fixture
def new_ecg_in_data() -> Dict:
    return deepcopy(ECGIn.Config.schema_extra.get("example"))


@pytest.fixture
def new_channel_in_data(
        new_ecg_in_data: Dict,
) -> Dict:
    return new_ecg_in_data["channels"][0]
