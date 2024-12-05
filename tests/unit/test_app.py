import boto3
import json
import os
import pytest
from unittest.mock import MagicMock
from moto import mock_aws

from send_s3.app import lambda_handler

BACKET1 = "s3-dummy-1"
DUMMY_PREFIX = "yyyy/MM/XXXXX.json"
DUMMY_DATA = "DUMMY-DATA"


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def s3(aws_credentials):
    """
    Return a mocked S3 client
    """
    with mock_aws():
        yield boto3.client("s3", region_name="us-east-1")


@pytest.fixture
def test_event():
    return {
        "body": json.dumps(
            {
                "toilet_id": "T001",
                "cat_id": "C001",
                "start_datetime": "2024-11-11 11:11:11",
                "end_datetime": "2024-11-11 11:11:11",
            }
        )
    }


@pytest.fixture
def lambda_context():
    """Create a mock for the Lambda context."""
    context = MagicMock()
    context.aws_request_id = "test-request-id"
    yield context


@pytest.fixture
def create_bucket_01(s3):
    s3.create_bucket(Bucket=BACKET1)


@pytest.mark.success
def test_lambda_handler_success(lambda_context, test_event, create_bucket_01):

    # Test the Lambda handler.
    response = lambda_handler(test_event, lambda_context.context)

    # Normal system testing
    assert response["statusCode"] == 201
    assert json.loads(response["body"])["message"] == "Data saved successfully"


@pytest.mark.exception
def test_lambda_handler_validateError(lambda_context):

    # Create an EVENT with no BODY.
    test_event = {"body": json.dumps({})}

    # Test the Lambda handler.
    response = lambda_handler(test_event, lambda_context.context)

    body = json.loads(response["body"])
    # Testing of anomalous systems.
    assert response["statusCode"] == 400
    # Assert that the error contains a specific string
    assert "Validation error" == body["error"]


@pytest.mark.exception
def test_lambda_handler_valueError(lambda_context):

    # Create an EVENT with no BODY.
    test_event = {"body": ""}

    # Test the Lambda handler.
    response = lambda_handler(test_event, lambda_context.context)

    body = json.loads(response["body"])
    # Testing of anomalous systems.
    assert response["statusCode"] == 400
    # Assert that the error contains a specific string
    assert "Value error" in body["error"]


@pytest.mark.exception
def test_lambda_handler_keyError(lambda_context):

    test_event = {"TEST": json.dumps({})}

    # Test the Lambda handler.
    response = lambda_handler(test_event, lambda_context.context)

    body = json.loads(response["body"])
    # Testing of anomalous systems.
    assert response["statusCode"] == 400
    # Assert that the error contains a specific string
    assert "Missing key" in body["error"]


@pytest.mark.exception
def test_lambda_handler_exception(test_event):

    context = {}

    # Test the Lambda handler.
    response = lambda_handler(test_event, context)

    body = json.loads(response["body"])
    # Testing of anomalous systems.
    assert response["statusCode"] == 500
    # Assert that the error contains a specific string
    assert "Exception" in body["error"]
