from rest_framework.exceptions import ValidationError


class InactiveAnnotatorError(ValidationError):
    default_detail = "Operation not allowed: Inactive Annotator"
    default_code = "inactive_annotator"
