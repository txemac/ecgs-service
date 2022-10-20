from typing import Any
from typing import Dict

import pytest
from pydantic import ValidationError

from api.ecg.domain.ecg import ChannelIn
from api.ecg.domain.ecg import ECGIn


def test_channel_in_ok(
        new_channel_in_data: Dict,
) -> None:
    assert ChannelIn(**new_channel_in_data)


@pytest.mark.parametrize(
    "attr",
    [
        "name",
        "signal",
    ]
)
def test_channel_in_pop(
        new_channel_in_data: Dict,
        attr: str,
) -> None:
    new_channel_in_data.pop(attr)
    with pytest.raises(ValidationError) as exception:
        ChannelIn(**new_channel_in_data)
    assert attr in str(exception.value)


@pytest.mark.parametrize(
    "attr, value",
    [
        ("name", None),
        ("name", ""),
        ("signal", None),
        ("signal", []),
        ("signal", ["a"]),
        ("num_samples", 0),
        ("num_samples", -1),
    ]
)
def test_channel_in_wrong(
        new_channel_in_data: Dict,
        attr: str,
        value: Any,
) -> None:
    new_channel_in_data[attr] = value
    with pytest.raises(ValidationError) as exception:
        ChannelIn(**new_channel_in_data)
    assert attr in str(exception.value)


def test_ecg_in_ok(
        new_ecg_in_data: Dict,
) -> None:
    assert ECGIn(**new_ecg_in_data)


@pytest.mark.parametrize(
    "attr",
    [
        "date",
        "channels",
    ]
)
def test_ecg_in_pop(
        new_ecg_in_data: Dict,
        attr: str,
) -> None:
    new_ecg_in_data.pop(attr)
    with pytest.raises(ValidationError) as exception:
        ECGIn(**new_ecg_in_data)
    assert attr in str(exception.value)


@pytest.mark.parametrize(
    "attr, value",
    [
        ("date", None),
        ("channels", ""),
        ("channels", None),
        ("channels", []),
        ("channels", [None]),
    ]
)
def test_ecg_in_wrong(
        new_ecg_in_data: Dict,
        attr: str,
        value: Any,
) -> None:
    new_ecg_in_data[attr] = value
    with pytest.raises(ValidationError) as exception:
        ECGIn(**new_ecg_in_data)
    assert attr in str(exception.value)
