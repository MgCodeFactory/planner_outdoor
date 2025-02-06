from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from po_app.auth_serializers import (
    CustomTokenObtainPairSerializer,
    CustomPasswordResetSerializer,
    CustomPasswordResetConfirmSerializer,
)
from .models import Users


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom class to ovveride simpleJWT obtain token view.
    """
    serializer_class = CustomTokenObtainPairSerializer


class CustomPasswordResetView(GenericAPIView):
    """
    Custom class for user reset password.
    """
    serializer_class = CustomPasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Method to create necessary uid and token for existing user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = Users.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            url = reverse("password-reset-confirm",
                          kwargs={"uid": uid, "token": token})

            reset_link = f"http://localhost:8080/#{url}"

            msg_html = render_to_string(
                "password_reset.html", {
                    "reset_link": reset_link, "user": user.username}
            )

            send_mail(
                "Password Reset Request",
                None,
                "noreply@po-team.com",
                [user.email],
                fail_silently=False,
                html_message=msg_html,
            )

            return response.Response(
                {
                    "message":
                    "An email has been send to your email address."
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {"error": "Invalid email user."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CustomPasswordResetConfirmView(GenericAPIView):
    """
    Custom class for reset confirm password procedure.
    """
    serializer_class = CustomPasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def patch(self, request, *args, **kwargs):
        """
        Final step to password reset procedure.
        """
        serializer = self.get_serializer(
            data=request.data, context={"kwargs": kwargs},)
        serializer.is_valid(raise_exception=True)
        return response.Response(
            {"message": "Password reset completed sucessfully."},
            status=status.HTTP_200_OK,
        )
