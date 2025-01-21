from rest_framework_simplejwt.views import TokenObtainPairView
from .auth_serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom class to ovveride simpleJWT obtain token view.
    """
    serializer_class = CustomTokenObtainPairSerializer
