import os

import boto3
import pytest
from moto import mock_aws

from layers.python.utils.s3_operation import S3Operation

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


# @pytest.fixture(scope="function")
# def mocked_aws(aws_credentials):
#     """
#     Mock all AWS interactions
#     Requires you to create your own boto3 clients
#     """
#     with mock_aws():
#         yield


@pytest.fixture
def create_bucket_01(s3):
    """Create an S3 bucket for Mock."""
    s3.create_bucket(Bucket=BACKET1)


# TEST1
def test_s3_bucket_creation_through_fixtures(create_bucket_01):
    """Check the number of S3 buckets created."""
    result = boto3.client("s3").list_buckets()

    assert len(result["Buckets"]) == 1


# TEST2
def test_S3Operation_save(create_bucket_01, s3):
    """
    Verify the save(put) function of the S3Operation class by mocking it.

    Args:
        create_bucket_01: fixture for create_bucket_01 function
        s3: s3 function fixture
    """

    model_instance = S3Operation(BACKET1, DUMMY_PREFIX, DUMMY_DATA)
    model_instance.save()
    response = s3.get_object(Bucket=BACKET1, Key=DUMMY_PREFIX)

    assert response["Body"].read().decode() == DUMMY_DATA


# TEST3
def test_S3Operation_Exception(create_bucket_01):
    """
    Exception test for S3Operation class.

    Args:
        create_bucket_01: fixture for create_bucket_01 function
    """

    model_instance = S3Operation("ERROR", DUMMY_PREFIX, DUMMY_DATA)
    response = model_instance.save()

    assert response["statusCode"] == 500
    assert "error" in response["body"]
