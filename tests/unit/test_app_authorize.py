import json
import pytest

from authorizer.app import lambda_handler
from unittest.mock import MagicMock

TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRkYVFKMzk1OHZZQkN5cVVJQVBIOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1xeTVnaGJ6YTdrend4cHVjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJEZEYxQXN2VU1uaUZXazB5czhoa1RMNzV3MUpUZUVCbkBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9oY3lja3Ztd20yLmV4ZWN1dGUtYXBpLmFwLW5vcnRoZWFzdC0xLmFtYXpvbmF3cy5jb20vIiwiaWF0IjoxNzMzMzYwMzI3LCJleHAiOjE3MzM0NDY3MjcsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6IkRkRjFBc3ZVTW5pRldrMHlzOGhrVEw3NXcxSlRlRUJuIn0.o3kHhJ_stxdgVxvxt-oPdvD8KDkagnQTEOOaV95tYwTTC5DsHQvye6ySBjX9JFmkw6ntLbTLAEBavFJk2F5v6IywPENBzSGrXGvg94ujVogyOA5kctA528ZOtWf97pEPgOUEW7_W7iWDg8VP-iiE597wu01KRz7UcXvghXaCwvVA5WsaGENLRkGSOTDgHI7ITMz2eO_QOFW1Qdm0G7CoKCtU8rNxcGfRPx242Q2UsqnWo3ezKBD9UWkXW9v7oDYFZVrwottmvXi36K1PifH4gP_geacteLbvhlw6H4YdIi84GX0uLROCwRjsoTpQgUJe5vxdRuLPmCYr_UAM7PUCew"


@pytest.fixture
def test_event():
    return {
        "type": "TOKEN",
        "authorizationToken": TOKEN,
        "methodArn": "",
    }


@pytest.fixture
def lambda_context():
    """Create a mock for the Lambda context."""
    context = MagicMock()
    yield context


@pytest.mark.success
def test_lambda_handler_success(test_event):

    # Test the Lambda handler.
    response = lambda_handler(test_event, lambda_context)

    # Normal system testing
    assert response


@pytest.mark.exception
def test_lambda_handler_exception(lambda_context):

    # Anticipated messages
    ERROR_MESSAGE = "Unauthorized"

    # Test the authenticate.
    with pytest.raises(Exception) as e:
        # Test the Lambda handler.
        lambda_handler("", lambda_context)

    # Assert Exception.
    assert str(e.value) == ERROR_MESSAGE
