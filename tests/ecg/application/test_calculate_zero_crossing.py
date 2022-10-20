from typing import List

import pytest

from api.ecg.application.calculate_zero_crossing import calculate_zero_crossing


@pytest.mark.parametrize(
    "signal, expected",
    (
            [[-1, 1], 1],
            [[-1, 1, -1], 2],
            [[-1, 1, 0], 2],
            [[-1, 0, -1], 2],
            [[1, -2, 3, -4, 5, -6, 7, -8, 9, -10], 9]
    )
)
def test_calculate_zero_crossing(
        signal: List[int],
        expected: int,
) -> None:
    assert calculate_zero_crossing(signal=signal) == expected
