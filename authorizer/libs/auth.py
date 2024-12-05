import logging
import os
import jwt
import json
import requests
from jose import jwt as jose_jwt
from dotenv import load_dotenv


# Obtained from the .env environment variable only when called locally.
if not os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
    load_dotenv(verbose=True)
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    print(dotenv_path)
    load_dotenv(dotenv_path)

# Get value from environment variable
AUDIENCE = os.getenv("AUDIENCE")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
TOKEN_ISSUER = f"https://{os.getenv("AUTH0_DOMAIN")}/"
JWKS_URI = f"https://{os.getenv("AUTH0_DOMAIN")}/.well-known/jwks.json"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_policy_document(effect, resource):
    """
    Function to generate policy document.

    Args:
        effect (str): Allow.
        resource (str): methodArn property of the event
            object of a Lambda function.

    Returns:
        dic: Policy Document.
    """

    logger.info("Execute get_policy_document.")

    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "execute-api:Invoke",
                "Effect": effect,
                "Resource": resource,
            }
        ],
    }


def extract_token(params):
    """
    Function to extract tokens.

    Args:
        params (dict): The event data passed to the Lambda function, containing
            details of the HTTP request.

    Returns:
        str: Token.
    """

    logger.info("Execute extract_token.")

    if params.get("type") != "TOKEN":

        logger.error('Expected "event.type" parameter to have value "TOKEN"')

        raise Exception(
            'Expected "event.type" parameter to have value "TOKEN"'
        )

    token_string = params.get("authorizationToken")
    if not token_string:

        logger.error('Expected "event.authorizationToken" parameter to be set')

        raise Exception(
            'Expected "event.authorizationToken" parameter to be set'
        )

    parts = token_string.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":

        logger.error(
            f'Invalid Authorization token - {token_string} does not match "Bearer .*"'
        )
        raise Exception(
            f'Invalid Authorization token - {token_string} does not match "Bearer .*"'
        )

    return parts[1]


def get_signing_key(kid):
    """
    Get signature keys from JWKs.

    Args:
        kid (str): Key identifier used for signature generation, etc.(kid)

    Returns:
        str: JWK Keys.

    Raises:
        Exception: Unable to find matching key with kid
    """

    logger.info("Execute get_signing_key.")

    response = requests.get(JWKS_URI)
    jwks = response.json()
    for key in jwks["keys"]:
        if key["kid"] == kid:
            return key

    logger.error(f"Unable to find matching key with kid {kid}")

    raise Exception(f"Unable to find matching key with kid {kid}")


def authenticate(event):
    """
    Authentication function.

    event (dict): The event data passed to the Lambda function, containing
        details of the HTTP request.

    Returns:
        dic: Policy and Context.

    Raises:
        Exception: Unauthorized
    """
    try:
        logger.info("Execute authenticate.")
        token = extract_token(event)
        unverified_header = jose_jwt.get_unverified_header(token)

        if not unverified_header or not unverified_header.get("kid"):
            raise Exception("Invalid token")

        key = get_signing_key(unverified_header["kid"])
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))

        # Validate tokens
        decoded = jose_jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=TOKEN_ISSUER,
        )

        # Return policy and context on success
        return {
            "principalId": decoded["sub"],
            "policyDocument": get_policy_document("Allow", event["methodArn"]),
            "context": {"scope": decoded.get("scope", "")},
        }

    except Exception as e:
        logger.error(f"Unauthorized: {e}")
        raise Exception(f"Unauthorized: {str(e)}")
