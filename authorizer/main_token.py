import os
from dotenv import load_dotenv

from layers.python.utils.token_utils import TokenUtils

# Obtained from the .env environment variable only when called locally.
if not os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
    load_dotenv(verbose=True)
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    print(dotenv_path)
    load_dotenv(dotenv_path)

# Get value from environment variable
AUDIENCE = os.getenv("AUDIENCE")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

if __name__ == "__main__":

    try:
        print("START")
        token_utils = TokenUtils(CLIENT_ID, CLIENT_SECRET, AUDIENCE, AUTH0_DOMAIN)

        token = token_utils.get_token()
        print(token)
        print("END")

    except Exception as e:
        print(f"Unauthorized {str(e)}")
