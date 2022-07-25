from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from spider.serializers import ProjectSerializer
from payment.serializers import SubscriptionSerializer


class SignupSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, required=True)
    name = serializers.CharField(max_length=100, required=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {"bad_token": "token is expired or invalid"}

    def validate(self, attr):
        self.token = attr["refresh"]
        return attr

    def save(self, **kwargs):
        #  print(self.token)
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class PasswordResetVerifiedSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=40)
    password = serializers.CharField(max_length=128)


class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)


class EmailChangeSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class EmailChangeVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True)
    subscription = SubscriptionSerializer(many=False)

    class Meta:
        model = get_user_model()
        fields = ("name", "email", "projects", 'subscription')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def to_seconds(self, timestr):
        seconds = 0
        for part in timestr.split(":"):
            seconds = seconds * 60 + int(part, 10)
        return seconds

    def validate(self, attrs):

        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["access_expires_in"] = self.to_seconds(
            str(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"])
        )
        data["refresh_expires_in"] = self.to_seconds(
            str(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"])
        )

        # Add extra responses here
        data["user"] = UserSerializer(self.user).data
        return data
