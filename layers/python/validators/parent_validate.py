class ParentValidator:
    """
    Parent class of all validations.
    """

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
            self.validate_data_types()
            self.validate_format_types()
        if self.errors:
            raise ValueError(f"Validation errors: {self.errors}")
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
        required_fields = []
        for field in required_fields:
            if field not in self.body:
                self.errors.append(
                    f"{field} is missing from the request body."
                )

    def validate_data_types(self):
        """
        Validate the data type of the parameters in the Body.
        Override to check each parameter.
        """
        pass

    def validate_format_types(self):
        """
        Validate the format of the parameters in the Body.
        Override to check each parameter.
        """
        pass
