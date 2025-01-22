from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import check_password
from rest_framework import serializers, exceptions
from django.utils.http import urlsafe_base64_decode
from .validators import CustomPasswordValidator
from .models import Users


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer override simple JWT obtain token.
    """
    username_field = "email"

    def validate(self, attrs):
        """
        Override validate method to add custom logic.
        """
        email = attrs.get("email")
        password = attrs.get("password")

        user = Users.objects.filter(email=email).first()

        if not user:
            raise exceptions.AuthenticationFailed(
                "No user found with the given credentials."
            )
        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                "User must be active to login.")

        if not check_password(password, user.password):
            raise exceptions.AuthenticationFailed(
                "Incorrect password.")

        refresh = self.get_token(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "user_id": user.id,
                "email": user.email,
            }
        }

        return data


class CustomPasswordResetSerializer(serializers.Serializer):
    """
    Custom serializer for password reset request.
    """
    email = serializers.EmailField(required=True)

    class Meta:
        model = Users
        fields = ["email"]


class CustomPasswordResetConfirmSerializer(serializers.Serializer):
    """
    Custom serializer for password reset confirmation.
    """
    new_password = serializers.CharField(
        write_only=True,
        max_length=128,
        required=True,
        validators=[CustomPasswordValidator()],
    )

    def validate(self, data):
        """
        Verify token and uid and then set new password.
        """
        new_password = data.get("new_password")
        token = self.context.get("kwargs").get("token")
        uid = self.context.get("kwargs").get("uid")

        if token is None or uid is None:
            raise serializers.ValidationError("Missing token or user ID.")

        pk = urlsafe_base64_decode(uid).decode()
        user = Users.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid.")

        user.set_password(new_password)
        user.save()
        return data

    class Meta:
        model = Users
        fields = ["new_password"]
