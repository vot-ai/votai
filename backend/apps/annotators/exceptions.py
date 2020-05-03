from rest_framework.exceptions import ValidationError


class InactiveAnnotatorError(ValidationError):
    default_detail = "Operation not allowed: Inactive Annotator"
    default_code = "inactive_annotator"


class AnnotatorsQuotaError(ValidationError):
    default_detail = "Operation not allowed: You have reached your quota of annotators"
    default_code = "annotators_quota"
