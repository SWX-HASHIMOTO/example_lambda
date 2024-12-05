import json
import logging

from datetime import datetime


class DateUtils(object):
    """Utils class for functions related to date and time"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def is_datetime(self, date_string=None):
        """
        Check date format and time.
        Type: %Y-%m-%d %H:%M:%S

        Returns: True
        Raises:
            ValueError: Return False
            TypeError: Return False
            Exception: Occurs when is_datetime fails.
        """
        self.logger.info("do is_datetime")
        try:
            # "yyyy-MM-dd hh:mm:ss" の形式で日付をパース
            datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False
        except TypeError:
            return False
        except Exception as e:
            self.logger.error(f"Error: is_datetime failed {e}")
            return {
                "statusCode": 500,
                "body": json.dumps(
                    {"error": "is_datetime failed", "details": str(e)}
                ),
            }
