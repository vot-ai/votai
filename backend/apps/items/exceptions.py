from rest_framework.exceptions import ValidationError


class ItemsQuotaError(ValidationError):
    default_detail = "Operation not allowed: You have reached your quota of items"
    default_code = "items_quota"
