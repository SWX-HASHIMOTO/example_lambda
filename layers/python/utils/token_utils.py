import json
import logging
import http.client


class TokenUtils(object):
    """
    Class that issues Token for Auth0.
    """

    def __init__(self, client_id, client_secret, audience, auth0_domain):
        self.client_id = client_id
        self.client_secret = client_secret
        self.audience = audience
        self.auth0_domain = auth0_domain
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def get_token(self):
        """
        Function get token from Auth0.

        Returns:
            str: Token with Bearer (Bearer .*)

        Exception:
            Outputs an error if the acquisition of a token fails.
        """

        try:
            self.logger.info("Token is issued.")

            # Create payload
            payload_dic = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "audience": self.audience,
                "grant_type": "client_credentials",
            }

            self.logger.info(
                f"HTTPS Request:(POST) https://{self.auth0_domain}/oauth/token"
            )
            # Obtain token by HTTP request to Auth0
            conn = http.client.HTTPSConnection(self.auth0_domain)
            payload = json.dumps(payload_dic)
            headers = {"content-type": "application/json"}
            conn.request("POST", "/oauth/token", payload, headers)
            res = conn.getresponse()
            data = res.read()

            # Edit token with type
            dic = json.loads(data)
            print(dic)
            token = f"{dic["token_type"]} {dic["access_token"]}"

            return token

        except http.client.HTTPException as e:
            # Handle HTTP-related errors.
            self.logger.error(f"Error: HTTP error occurred {e}")

            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"error": "HTTP error occurred", "details": str(e)}
                ),
            }

        except Exception as e:
            # Other Error
            self.logger.error(f"Error: Get token failed {e}")

            return {
                "statusCode": 500,
                "body": json.dumps(
                    {"error": "Get token failed", "details": str(e)}
                ),
            }
