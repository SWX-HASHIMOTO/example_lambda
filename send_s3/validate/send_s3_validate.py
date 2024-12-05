from validators.parent_send_validate import ParentSendValidator
from exceptions.extra_exception import ValidateError
from utils.date_utils import DateUtils


class SendS3Validator(ParentSendValidator):
    """
    This class inherits from the layer ParentSendValidator
    and performs validation before sending data to S3.
    If validate is NG, it is stored with the message in the errors array.
    """

    def validate(self):
        if self.is_body():
            self.validate_presence()
            self.validate_extra_presence()
            if not self.errors:
                self.validate_format_types()
                self.validate_extra_format_types()

        if self.errors:
            raise ValidateError(self.errors)
        return True

    def validate_extra_presence(self):
        """
        Make sure that Body has parameters other than inherited items.
        Set additional parameters in required_fields.
        """
        required_fields = ["start_datetime", "end_datetime"]
        for field in required_fields:
            if field not in self.body:
                self.errors.append(
                    f"{field} is missing from the request body."
                )

    def validate_extra_format_types(self):
        """
        Validate the format of additional parameters.
        """

        date_utils = DateUtils()

        if not date_utils.is_datetime(self.body["start_datetime"]):
            self.errors.append(
                f"Invalid start_datetime format.[{self.body['start_datetime']}]"
            )

        if not date_utils.is_datetime(self.body["end_datetime"]):
            self.errors.append(
                f"Invalid end_datetime format.[{self.body['end_datetime']}]"
            )
