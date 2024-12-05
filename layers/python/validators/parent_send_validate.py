import re
from exceptions.extra_exception import ValidateError


class ParentSendValidator(object):
    def __init__(self, body):
        self.body = body
        self.errors = []

    def validate(self):
        """
        Each validation is performed by calling this function.
        When you add a new validation, add it to this function as well as.
        """
        if self.is_body():
            self.validate_presence()
            if not self.errors:
                self.validate_format_types()
        if self.errors:
            raise ValidateError(self.errors)
        return True

    def is_body(self):
        """
        Validation of the Body itself.
        """
        if not self.body:
            self.errors.append("body is missing from the request")
            return False
        else:
            return True

    def validate_presence(self):
        """
        Parameters required for Body but to be verified.
        Set the necessary items in Body to an array by overriding,
        and check them.
        """
        required_fields = ["toilet_id", "cat_id"]
        for field in required_fields:
            if field not in self.body:
                self.errors.append(
                    f"{field} is missing from the request body."
                )

    def validate_format_types(self):
        """
        Validate data types for parameters.
        """
        if not re.match(
            r"T(?:00[1-9]|0[1-9][0-9]|[1-9][0-9]{2})$", self.body["toilet_id"]
        ):
            self.errors.append(
                f"Invalid ToiletID format.[{self.body['toilet_id']}]"
            )
        if not re.match(
            r"C(?:00[1-9]|0[1-9][0-9]|[1-9][0-9]{2})$", self.body["cat_id"]
        ):
            self.errors.append(f"Invalid CatID format.[{self.body['cat_id']}]")
