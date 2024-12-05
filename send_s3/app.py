import json
import os

import datetime
import logging

try:
    from validate.send_s3_validate import SendS3Validator
except ImportError:
    from .validate.send_s3_validate import SendS3Validator

from utils.s3_operation import S3Operation
from exceptions.extra_exception import ValidateError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

BUCKET_NAME = os.environ.get("BUCKET_NAME")


def lambda_handler(event, context):
    """AWS Lambda handler function.

    Entry point for AWS Lambda functions called by API Gateway or
    other services.

    Args:
        event (dict): The event data passed to the Lambda function, containing
            details of the HTTP request.
        context (LambdaContext): The runtime context for the Lambda function,
            including the request ID.
    Returns:
        dict: A response with a status code and a message indicating success
            or failure.

    Raises:
        ValidateError: Original Error. If verification fails,
            an error is assumed.
        ValueError: If the input data is invalid.
        KeyError: This is sent when a key in the mapping (dictionary) is
            not found.
        Exception: For any other general exceptions.
    """
    try:
        logger.info("Lambda function has started.")

        # Get data from the body of the request
        body = json.loads(event["body"])
        logger.info(f"Request body: {body}")

        logger.info("Validate send Data.")
        # Validate body
        validator = SendS3Validator(body)
        validator.validate()

        # Convert UTC to JST (UTC+9)
        jst = datetime.timezone(datetime.timedelta(hours=9))

        # Get the current date and time in JST
        now = datetime.datetime.now(jst)
        logger.info(f"Current JST time: {now}")

        # Create a prefix based on current date
        prefix = f"{now.year}/{now.month:02d}/"

        # Create filename with prefix
        file_name = f"{prefix}data-{context.aws_request_id}.json"
        logger.info(f"Generated file name: {file_name}")

        # Save to S3
        s3 = S3Operation(BUCKET_NAME, file_name, json.dumps(body))
        s3.save()

        logger.info(f"Data saved to S3 bucket {BUCKET_NAME} with key {file_name}")

        # Success Response
        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Data saved successfully"}),
        }

    except ValidateError as e:
        logger.error(f"{e}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Validation error", "errors": e.errors}),
        }

    except ValueError as e:
        logger.error(f"Value error {e}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Value error {str(e)}"}),
        }

    except KeyError as e:
        logger.error(f"Missing key error: {e}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Missing key {str(e)}"}),
        }

    except Exception as e:
        logger.exception(f"Exception: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Exception {str(e)}"}),
        }
