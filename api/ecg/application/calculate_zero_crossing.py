from typing import List


def calculate_zero_crossing(
        signal: List[int],
) -> int:
    """
    Calculate the number of cross zero in a signal.

    :param signal: signal
    :return: number of zero crossing
    """
    result = 0
    for index in range(len(signal) - 1):
        result += 1 if signal[index] * signal[index + 1] <= 0 else 0

    return result
