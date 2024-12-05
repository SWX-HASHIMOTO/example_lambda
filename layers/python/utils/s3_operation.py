import boto3
import json
import logging


class S3Operation(object):
    """S3Operation Class.

    Class that aggregates S3 operations (PUT, GET, etc.)
    """

    def __init__(self, bucket, file_name, body):
        self.bucket = bucket
        self.file_name = file_name
        self.body = body
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def save(self):
        """AWS Lambda handler function.

        Entry point for AWS Lambda functions called by API Gateway or
        other services.

        Exception:
            Occurs when save to S3 fails.
        """
        self.logger.info("save to S3")
        try:
            s3 = boto3.client("s3", region_name="ap-northeast-1")
            s3.put_object(
                Bucket=self.bucket, Key=self.file_name, Body=self.body
            )

        except Exception as e:
            self.logger.error(f"Error: S3 save failed {e}")

            return {
                "statusCode": 500,
                "body": json.dumps(
                    {"error": "S3 save failed", "details": str(e)}
                ),
            }
