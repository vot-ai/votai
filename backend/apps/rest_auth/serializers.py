from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from dj_rest_auth import serializers as dj_serializers
from dj_rest_auth.registration import serializers as dj_social_serializers


UserModel = get_user_model()


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("username", "email", "first_name", "last_name")
        read_only_fields = ("email",)


class PasswordResetSerializer(dj_serializers.PasswordResetSerializer):
    email = serializers.CharField()


class RegistrationSerializer(dj_social_serializers.RegisterSerializer):
    email = serializers.CharField()
