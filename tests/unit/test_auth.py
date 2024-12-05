import json
import pytest
from unittest.mock import patch

from authorizer.libs.auth import authenticate
from authorizer.libs.auth import get_signing_key

# from unittest.mock import MagicMock

TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRkYVFKMzk1OHZZQkN5cVVJQVBIOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1xeTVnaGJ6YTdrend4cHVjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJEZEYxQXN2VU1uaUZXazB5czhoa1RMNzV3MUpUZUVCbkBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9oY3lja3Ztd20yLmV4ZWN1dGUtYXBpLmFwLW5vcnRoZWFzdC0xLmFtYXpvbmF3cy5jb20vIiwiaWF0IjoxNzMzMzYwMzI3LCJleHAiOjE3MzM0NDY3MjcsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6IkRkRjFBc3ZVTW5pRldrMHlzOGhrVEw3NXcxSlRlRUJuIn0.o3kHhJ_stxdgVxvxt-oPdvD8KDkagnQTEOOaV95tYwTTC5DsHQvye6ySBjX9JFmkw6ntLbTLAEBavFJk2F5v6IywPENBzSGrXGvg94ujVogyOA5kctA528ZOtWf97pEPgOUEW7_W7iWDg8VP-iiE597wu01KRz7UcXvghXaCwvVA5WsaGENLRkGSOTDgHI7ITMz2eO_QOFW1Qdm0G7CoKCtU8rNxcGfRPx242Q2UsqnWo3ezKBD9UWkXW9v7oDYFZVrwottmvXi36K1PifH4gP_geacteLbvhlw6H4YdIi84GX0uLROCwRjsoTpQgUJe5vxdRuLPmCYr_UAM7PUCew"
TOKEN_EXPIRED = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRkYVFKMzk1OHZZQkN5cVVJQVBIOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1xeTVnaGJ6YTdrend4cHVjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJ2dGdQakxSMDgzbVRMT3l3UHJqZFZvaFRLb21CMTdXTUBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly85Y21mMXBwNWo1LmV4ZWN1dGUtYXBpLmFwLW5vcnRoZWFzdC0xLmFtYXpvbmF3cy5jb20vIiwiaWF0IjoxNzI5NTc3OTQ5LCJleHAiOjE3Mjk2NjQzNDksImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6InZ0Z1BqTFIwODNtVExPeXdQcmpkVm9oVEtvbUIxN1dNIn0.Af2d4XT0aMBf2x8Ibi0cWP2fCXvk_XMyy6MSgd9eZigjHNAMK5Egnz2CcDAlhGuOn-7xAnt2K8BFlKpT5msg9gqNbSiYSlhAu8k7fFwu4mTztCDCHA4s8cD0EZJ9z8RbGOgH9Ya8NrURALzkNQnp8D7ziYWEfS5B30ItX1I3jk0XKbABxjKDuu6QdIPaNhJw8VSBX60oHArJozKbPLu5z07syNrk14iIqw2NwPSuSXx6z8CP8hozTk9ji7Zbcr3OReyZymfoVHQiGm8EMJlG70RvJrjBtwPEOO0Cq8QoG-Wcj1oeiDC1MsdN-0LeBPeWJWzxVkEiTE-l0jWb5S8oZA"


@pytest.fixture
def test_event():
    return {
        "type": "TOKEN",
        "authorizationToken": TOKEN,
        "methodArn": "TESTARN",
    }


@pytest.fixture
def test_event_error1():
    return {
        "authorizationToken": "",
        "methodArn": "TESTARN",
    }


@pytest.fixture
def test_event_error2():
    return {
        "type": "TOKEN",
        "authorizationToken": 1,
        "methodArn": "TESTARN",
    }


@pytest.fixture
def test_event_error3():
    return {
        "type": "TOKEN",
        "authorizationToken": None,
        "methodArn": "TESTARN",
    }


@pytest.fixture
def test_event_error4():
    return {
        "type": "TOKEN",
        "authorizationToken": "TEST",
        "methodArn": "TESTARN",
    }


@pytest.fixture
def test_event_error5():
    return {
        "type": "TOKEN",
        "authorizationToken": "Bearer AAAAAA",
        "methodArn": "TESTARN",
    }


@pytest.fixture
def test_event_error6():
    return {
        "type": "TOKEN",
        "authorizationToken": TOKEN_EXPIRED,
        "methodArn": "TESTARN",
    }


# @pytest.fixture
# def lambda_context():
#     """Create a mock for the Lambda context."""
#     context = MagicMock()
#     yield context


@pytest.mark.success
def test_validator_success(test_event):

    assert1 = "DdF1AsvUMniFWk0ys8hkTL75w1JTeEBn@clients"
    assert2 = "2012-10-17"
    assert3 = "execute-api:Invoke"
    assert4 = "TESTARN"
    assert5 = "Allow"
    assert6 = ""

    # Execute authenticate
    response = authenticate(test_event)

    # assert
    assert response["principalId"] == assert1
    assert response["policyDocument"]["Version"] == assert2
    assert response["policyDocument"]["Statement"][0]["Action"] == assert3
    assert response["policyDocument"]["Statement"][0]["Resource"] == assert4
    assert response["policyDocument"]["Statement"][0]["Effect"] == assert5
    assert response["context"]["scope"] == assert6


@pytest.mark.exception
def test_auth_exception1(test_event_error1):

    # Anticipated messages
    ERROR_MESSAGE = 'Unauthorized: Expected "event.type" parameter to have value "TOKEN"'

    # Test the authenticate.
    with pytest.raises(Exception) as e:
        authenticate(test_event_error1)

    # Assert Exception.
    assert str(e.value) == ERROR_MESSAGE


@pytest.mark.exception
def test_authenticate_exception2(test_event_error2):

    # Anticipated messages
    ERROR_MESSAGE = "Unauthorized: 'int' object has no attribute 'split'"

    # Test the authenticate.
    with pytest.raises(Exception) as e:
        authenticate(test_event_error2)

    # Assert Exception.
    assert str(e.value) == ERROR_MESSAGE


@pytest.mark.exception
def test_authenticate_exception3(test_event_error3):

    # Anticipated messages
    ERROR_MESSAGE = 'Unauthorized: Expected "event.authorizationToken" parameter to be set'

    # Test the authenticate.
    with pytest.raises(Exception) as e:
        authenticate(test_event_error3)

    # Assert Exception.
    assert str(e.value) == ERROR_MESSAGE


@pytest.mark.exception
def test_authenticate_exception4(test_event_error4):

    # Anticipated messages
    ERROR_MESSAGE = 'Unauthorized: Invalid Authorization token - TEST does not match "Bearer .*"'

    # Test the authenticate.
    with pytest.raises(Exception) as e:
        authenticate(test_event_error4)

    # Assert Exception.
    assert str(e.value) == ERROR_MESSAGE


@pytest.mark.exception
def test_authenticate_exception5(test_event_error5):

    # Anticipated messages
    ERROR_MESSAGE = "Unauthorized: Error decoding token headers."

    # Test the authenticate.
    with pytest.raises(Exception) as e:
        authenticate(test_event_error5)

    # Assert Exception.
    assert str(e.value) == ERROR_MESSAGE


@pytest.mark.exception
def test_authenticate_exception6(test_event_error6):
    """
    Perform expiration testing.
    """

    # Anticipated messages
    ERROR_MESSAGE = "Unauthorized: Signature has expired."

    # Test the authenticate.
    with pytest.raises(Exception) as e:
        authenticate(test_event_error6)

    # Assert Exception.
    assert str(e.value) == ERROR_MESSAGE


@pytest.mark.exception
@patch("authorizer.libs.auth.jose_jwt.get_unverified_header")
def test_authenticate_exception7(mock_get_unverified_header, test_event):
    """
    Mock up .jose_jwt.get_unverified_header and raise an Exception.
    """
    mock_get_unverified_header.return_value = None  # Set unverified_header None.

    # Test the authenticate.
    with pytest.raises(Exception) as e:
        authenticate(test_event)

    # Assert Exception.
    assert str(e.value) == "Unauthorized: Invalid token"


@pytest.mark.get_signing_key_exception
def test_get_signing_key_exception8():
    """
    Exception test for get_signing_key function.
    """

    # Anticipated messages
    ERROR_MESSAGE = "Unable to find matching key with kid"

    kid = {"kid": "TEST"}

    # Test the authenticate.
    with pytest.raises(Exception) as e:
        get_signing_key(kid)

    # Assert for inclusion in Exception.
    assert ERROR_MESSAGE in str(e.value)
