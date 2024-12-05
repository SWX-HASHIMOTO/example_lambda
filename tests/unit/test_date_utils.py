from layers.python.utils.date_utils import DateUtils


def test_is_datetime():

    date_utils = DateUtils()

    result = date_utils.is_datetime("2024-01-01 11:33:44")

    assert result


def test_is_datetime_NG1():

    date_utils = DateUtils()

    result = date_utils.is_datetime("あいうえお")

    assert not result


def test_is_datetime_NG2():

    date_utils = DateUtils()

    result = date_utils.is_datetime(1)

    assert not result
