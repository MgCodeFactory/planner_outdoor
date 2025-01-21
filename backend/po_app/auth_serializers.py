from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, exceptions
from po_app.models import Users
from django.contrib.auth.hashers import check_password


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
                "No user found with the given credentials"
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
