from typing import Any
from typing import Dict

import pytest
from pydantic import ValidationError

from src.ecg.domain.ecg import Channel
from src.ecg.domain.ecg import ECG


def test_channel_ok(
        new_channel_data: Dict,
) -> None:
    assert Channel(**new_channel_data)


@pytest.mark.parametrize(
    "attr",
    [
        "name",
        "signal",
    ]
)
def test_channel_pop(
        new_channel_data: Dict,
        attr: str,
) -> None:
    new_channel_data.pop(attr)
    with pytest.raises(ValidationError) as exception:
        Channel(**new_channel_data)
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
def test_channel_wrong(
        new_channel_data: Dict,
        attr: str,
        value: Any,
) -> None:
    new_channel_data[attr] = value
    with pytest.raises(ValidationError) as exception:
        Channel(**new_channel_data)
    assert attr in str(exception.value)


def test_ecg_ok(
        new_ecg_data: Dict,
) -> None:
    assert ECG(**new_ecg_data)


@pytest.mark.parametrize(
    "attr",
    [
        "date",
        "channels",
    ]
)
def test_ecg_pop(
        new_ecg_data: Dict,
        attr: str,
) -> None:
    new_ecg_data.pop(attr)
    with pytest.raises(ValidationError) as exception:
        ECG(**new_ecg_data)
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
def test_ecg_wrong(
        new_ecg_data: Dict,
        attr: str,
        value: Any,
) -> None:
    new_ecg_data[attr] = value
    with pytest.raises(ValidationError) as exception:
        ECG(**new_ecg_data)
    assert attr in str(exception.value)
