from datetime import datetime
from uuid import UUID


def assert_dicts(original, expected):
    """
    Assert that check that the dict body contains all keys in expected.
    And the values are the same.
    If a value in expected contains "*" the value in body can be any value.
    If a value is a dict, check the dict inside.
    If a value is a list, check the list inside.
    :param Dict original: original dict
    :param Dict expected: expected dict
    """
    original.pop("_sa_instance_state") if "_sa_instance_state" in original.keys() else None
    expected.pop("_sa_instance_state") if "_sa_instance_state" in expected.keys() else None
    for key in expected.keys():
        assert key in original.keys(), key
        if isinstance(original[key], dict):
            assert isinstance(expected[key], dict)
            assert_dicts(original=original[key], expected=expected[key])
        elif isinstance(original[key], list):
            assert isinstance(expected[key], list)
            assert_lists(original=original[key], expected=expected[key])
        elif (isinstance(original[key], datetime) or isinstance(expected[key], datetime)) and expected[key] != "*":
            assert_datetime(key=key, original=original[key], expected=expected[key])
        elif (isinstance(original[key], UUID) or isinstance(expected[key], UUID)) and expected[key] != "*":
            assert str(original[key]) == str(expected[key]), f"key: {key}: {original[key]} - {expected[key]}"
        elif not expected[key] == "*":
            assert original[key] == expected[key], f"key: {key}: {original[key]} - {expected[key]}"


def assert_lists(original, expected, sort=None):
    """
    Assert that check to lists. Check the len of both list and the content.
    :param List original: original list
    :param List expected: expected list
    :param str sort: sort objects list by sort field.
    """
    assert len(original) == len(expected), len(original)

    if sort is not None and isinstance(original[0], dict):
        original = sorted(original, key=lambda x: x[sort])
        expected = sorted(expected, key=lambda x: x[sort])
    elif sort is not None:
        original = sorted(original, key=lambda x: x.__getattribute__(sort))
        expected = sorted(expected, key=lambda x: x.__getattribute__(sort))

    for i in range(len(original)):
        if original[i] == expected[i]:
            pass
        elif isinstance(original[i], dict):
            assert isinstance(expected[i], dict), type(expected[i])
            assert_dicts(original=original[i], expected=expected[i])
        elif isinstance(original[i], list):
            assert isinstance(expected[i], list), type(expected[i])
            assert_lists(original=original[i], expected=expected[i])
        elif not expected[i] == "*":
            assert original[i] == expected[i], original[i]


def assert_datetime(key, original, expected):
    """
    Assert dates values.
    :param key: name of the field
    :param original: original
    :param expected: expected
    """
    if not isinstance(original, str):
        original = datetime.isoformat(original)

    if not isinstance(expected, str):
        expected = datetime.isoformat(expected)

    assert original.replace("T", " ")[:19] == expected.replace("T", " ")[:19], key
