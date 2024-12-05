import logging

try:
    from libs.auth import authenticate
except ImportError:
    from .libs.auth import authenticate

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """AWS Lambda handler function.

    Entry point for AWS Lambda functions called by API Gateway or
    other services.
    Used by Lambda Authorizer to authenticate with Auth0.

    Args:
        event (dict): The event data passed to the Lambda function, containing
            details of the HTTP request.
        context (LambdaContext): The runtime context for the Lambda function,
            including the request ID.
    Returns:
        dict: A response with a status code and a message indicating success
            or failure.

    Raises:
        Exception: For any other general exceptions.
            Raise Exception to Authorizer.
    """
    try:
        logger.info("Lambda function has started.")

        data = authenticate(event)
        return data

    except Exception as e:
        logger.exception(e)
        # Raise Exception to Authorizer
        raise Exception("Unauthorized")
