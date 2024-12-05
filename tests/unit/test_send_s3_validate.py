import pytest

from send_s3.validate.send_s3_validate import (
    SendS3Validator,
)


@pytest.fixture
def test_event1():
    return {
        "toilet_id": "T001",
        "cat_id": "C001",
        "start_datetime": "0001-01-01 00:00:00",
        "end_datetime": "0001-01-01 00:00:00",
    }


@pytest.fixture
def test_event2():
    return {
        "toilet_id": "T999",
        "cat_id": "C999",
        "start_datetime": "9999-12-31 23:59:59",
        "end_datetime": "9999-12-31 23:59:59",
    }


@pytest.fixture
def test_event3():
    return {
        "toilet_id": "T999",
        "cat_id": "C999",
        "start_datetime": "9999-12-31 23:59:59",
        "end_datetime": "9999-12-31 23:59:59",
    }


@pytest.mark.success
def test_validator_success_1(test_event1):
    validator = SendS3Validator(test_event1)
    response = validator.validate()
    assert response


@pytest.mark.success
def test_validator_success_2(test_event2):
    validator = SendS3Validator(test_event2)
    response = validator.validate()
    assert response


@pytest.mark.anything_missing
def test_validator_body_missing():

    validator = SendS3Validator({})

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['body is missing from the request']"


@pytest.mark.anything_missing
def test_validator_toilet_id_missing(test_event3):

    del test_event3["toilet_id"]

    validator = SendS3Validator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['toilet_id is missing from the request body.']"


@pytest.mark.anything_missing
def test_validator_cat_id_missing(test_event3):

    del test_event3["cat_id"]

    validator = SendS3Validator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['cat_id is missing from the request body.']"


@pytest.mark.anything_missing
def test_validator_start_datetime_missing(test_event3):

    del test_event3["start_datetime"]

    validator = SendS3Validator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['start_datetime is missing from the request body.']"


@pytest.mark.anything_missing
def test_validator_end_datetime_missing(test_event3):

    del test_event3["end_datetime"]

    validator = SendS3Validator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['end_datetime is missing from the request body.']"


@pytest.mark.validate_ng
@pytest.mark.skipif(True, reason="[Testing at the Inherited Source]")
def test_validator_toilet_id_ng1(test_event3):

    test_event3["toilet_id"] = "T000"

    validator = SendS3Validator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid ToiletID format.[T000]']"


@pytest.mark.validate_ng
@pytest.mark.skipif(True, reason="[Testing at the Inherited Source]")
def test_validator_toilet_id_ng2(test_event3):

    test_event3["toilet_id"] = "T00"

    validator = SendS3Validator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid ToiletID format.[T00]']"


@pytest.mark.validate_ng
@pytest.mark.skipif(True, reason="[Testing at the Inherited Source]")
def test_validator_toilet_id_ng3(test_event3):

    test_event3["toilet_id"] = "A001"

    validator = SendS3Validator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid ToiletID format.[A001]']"


@pytest.mark.validate_ng
@pytest.mark.skipif(True, reason="[Testing at the Inherited Source]")
def test_validator_cat_id_ng1(test_event3):

    test_event3["cat_id"] = "C000"

    validator = SendS3Validator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid CatID format.[C000]']"


@pytest.mark.validate_ng
@pytest.mark.skipif(True, reason="[Testing at the Inherited Source]")
def test_validator_cat_id_ng2(test_event3):

    test_event3["cat_id"] = "C00"

    validator = SendS3Validator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid CatID format.[C00]']"


@pytest.mark.validate_ng
@pytest.mark.skipif(True, reason="[Testing at the Inherited Source]")
def test_validator_cat_id_ng3(test_event3):

    test_event3["cat_id"] = "A001"

    validator = SendS3Validator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid CatID format.[A001]']"


@pytest.mark.validate_ng
def test_validator_start_datetime_ng1(test_event3):

    test_event3["start_datetime"] = "0000-01-01 00:00:00"

    validator = SendS3Validator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid start_datetime format.[0000-01-01 00:00:00]']"


@pytest.mark.validate_ng
def test_validator_start_datetime_ng2(test_event3):

    test_event3["start_datetime"] = "あいうえお"

    validator = SendS3Validator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid start_datetime format.[あいうえお]']"


@pytest.mark.validate_ng
def test_validator_end_datetime_ng1(test_event3):

    test_event3["end_datetime"] = "0000-01-01 00:00:00"

    validator = SendS3Validator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid end_datetime format.[0000-01-01 00:00:00]']"


@pytest.mark.validate_ng
def test_validator_end_datetime_ng2(test_event3):

    test_event3["end_datetime"] = "あいうえお"

    validator = SendS3Validator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid end_datetime format.[あいうえお]']"
