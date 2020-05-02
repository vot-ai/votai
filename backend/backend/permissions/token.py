from rest_framework.permissions import BasePermission


class HasValidToken(BasePermission):
    """Has Valid Token

    Checks if the request has a valid token,
    even if the user is not authenticated
    """

    def has_permission(self, request, view):
        return bool(getattr(request, "auth", False))
