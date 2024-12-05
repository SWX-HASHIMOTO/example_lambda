# import json
import datetime
import os

from send_s3.validate.send_s3_validate import (
    SendS3Validator,
)
from exceptions.extra_exception import ValidateError

# from common.s3_operation import S3Operation

if __name__ == "__main__":

    print("START")
    body = {
        "toilet_id": "001",
        "cat_id": "C000",
        "start_datetime": "2024-11-11 11:11:11",
        "end_datetime": "2024-11-11 11:11:11",
    }

    try:
        BUCKET_NAME = os.environ.get("BUCKET_NAME")
        print("BUCKET_NAME:", BUCKET_NAME)
        test = SendS3Validator(body)

        # Convert UTC to JST (UTC+9)
        jst = datetime.timezone(datetime.timedelta(hours=9))

        # Get the current date and time in JST
        now = datetime.datetime.now(jst)

        # Create a prefix based on current date
        prefix = f"{now.year}/{now.month:02d}/"

        test.validate()

        # Create filename with prefix
        file_name = f"{prefix}data.json"
        # s3 = S3Operation("", file_name, json.dumps(body))
        # s3.save()

        print("Success")

    except ValueError as e:
        print(f"Value errors: {e.errors}")

    except ValidateError as e:
        print(e.errors)

    except Exception as e:
        print(e)
