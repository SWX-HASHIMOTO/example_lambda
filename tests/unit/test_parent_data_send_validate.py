import pytest

from layers.python.validators.parent_send_validate import ParentSendValidator


@pytest.fixture
def test_event1():
    return {
        "toilet_id": "T001",
        "cat_id": "C001",
    }


@pytest.fixture
def test_event2():
    return {
        "toilet_id": "T999",
        "cat_id": "C999",
    }


@pytest.fixture
def test_event3():
    return {
        "toilet_id": "T999",
        "cat_id": "C999",
    }


def test_validator_success_1(test_event1):
    validator = ParentSendValidator(test_event1)
    response = validator.validate()
    assert response


def test_validator_success_2(test_event2):
    validator = ParentSendValidator(test_event2)
    response = validator.validate()
    assert response


def test_validator_body_missing():

    validator = ParentSendValidator({})

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['body is missing from the request']"


def test_validator_toilet_id_missing(test_event3):

    del test_event3["toilet_id"]

    validator = ParentSendValidator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['toilet_id is missing from the request body.']"


def test_validator_cat_id_missing(test_event3):

    del test_event3["cat_id"]

    validator = ParentSendValidator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['cat_id is missing from the request body.']"


def test_validator_toilet_id_ng1(test_event3):

    test_event3["toilet_id"] = "T000"

    validator = ParentSendValidator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid ToiletID format.[T000]']"


def test_validator_toilet_id_ng2(test_event3):

    test_event3["toilet_id"] = "T00"

    validator = ParentSendValidator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid ToiletID format.[T00]']"


def test_validator_toilet_id_ng3(test_event3):

    test_event3["toilet_id"] = "A001"

    validator = ParentSendValidator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid ToiletID format.[A001]']"


def test_validator_cat_id_ng1(test_event3):

    test_event3["cat_id"] = "C000"

    validator = ParentSendValidator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid CatID format.[C000]']"


def test_validator_cat_id_ng2(test_event3):

    test_event3["cat_id"] = "C00"

    validator = ParentSendValidator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid CatID format.[C00]']"


def test_validator_cat_id_ng3(test_event3):

    test_event3["cat_id"] = "A001"

    validator = ParentSendValidator(test_event3)

    with pytest.raises(Exception) as e:
        validator.validate()

    assert str(e.value) == "['Invalid CatID format.[A001]']"
