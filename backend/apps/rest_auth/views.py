from rest_framework.permissions import AllowAny
from rest_framework import exceptions
from dj_rest_auth import views as dj_views
from dj_rest_auth import serializers as dj_serializers
from dj_rest_auth.registration import views as dj_social_views
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    UserDetailsSerializer,
    PasswordResetSerializer,
    RegistrationSerializer,
)


class LoginView(dj_views.LoginView):
    swagger_tags = ["User"]

    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: dj_serializers.JWTSerializer}, security=[])
    def post(self, *args, **kwargs):
        """Get token from password

        Takes using username/email and password, and returns JWT tokens
        """
        return super().post(*args, **kwargs)


class LogoutView(dj_views.LogoutView):
    swagger_tags = ["User"]

    @swagger_auto_schema(responses={}, deprecated=True)
    def get(self, *args, **kwargs):
        """GET revoke token

        Logouts using GET are no longer supported
        """
        raise exceptions.MethodNotAllowed("GET")

    @swagger_auto_schema(responses={200: "Logout successful"},)
    def post(self, *args, **kwargs):
        """Revoke token

        Logs the user out and revokes the current token
        """
        return super().post(*args, **kwargs)


class UserDetailsView(dj_views.UserDetailsView):
    swagger_tags = ["User"]

    serializer_class = UserDetailsSerializer

    def get(self, *args, **kwargs):
        """Get user details

        Returns details from the current user
        """
        return super().get(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Update user details

        Updates all fields from the user
        """
        return super().put(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Partially update user details

        Updates some fields from the user
        """
        return super().patch(*args, **kwargs)


class PasswordResetView(dj_views.PasswordResetView):
    swagger_tags = ["User"]

    @swagger_auto_schema(
        responses={200: "Password reset e-mail has been sent."},
        request_body=PasswordResetSerializer,
    )
    def post(self, *args, **kwargs):
        """Password reset

        Sends an email to the user with instructions on how to reset the password
        """
        return super().post(*args, **kwargs)


class PasswordResetConfirmView(dj_views.PasswordResetConfirmView):
    swagger_tags = ["User"]

    @swagger_auto_schema(
        responses={
            200: "Password has been reset with the new password.",
            400: "Request data is missing or incorrect",
        }
    )
    def post(self, *args, **kwargs):
        """Password reset confirmation

        Takes a token and uid that will have arrived by email and the new password as parameters to reset the user's password.
        """
        return super().post(*args, **kwargs)


class PasswordChangeView(dj_views.PasswordChangeView):
    swagger_tags = ["User"]

    @swagger_auto_schema(
        responses={
            200: "New password has been saved.",
            400: "Request data is missing or incorrect",
        }
    )
    def post(self, *args, **kwargs):
        """Password change

        Changes the authenticated user's password
        """
        return super().post(*args, **kwargs)


class RegistrationView(dj_social_views.RegisterView):
    swagger_tags = ["User"]

    @swagger_auto_schema(
        request_body=RegistrationSerializer,
        responses={201: "Verification e-mail sent."},
    )
    def post(self, *args, **kwargs):
        """Register new user

        Use this endpoint to register a new user using a username/email and password
        """
        return super().post(*args, **kwargs)


class VerifyEmailView(dj_social_views.VerifyEmailView):
    swagger_tags = ["User"]

    @swagger_auto_schema(
        responses={200: "Email verified", 400: "Incorrect verification key"},
    )
    def post(self, *args, **kwargs):
        """Verify email

        Verify a user's email given a key
        """
        return super().post(*args, **kwargs)
