from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .validators import (
    CustomUsernameValidator,
    CustomPasswordValidator,
    CustomNameValidator,
    CustomDescriptionValidator,
    CustomLocationValidator,
)


class ValidationRulesView(GenericAPIView):
    """
    View to get validation rules for the application.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        return help_text messages from different validators.
        """
        return Response({
            "username_rules": CustomUsernameValidator().get_help_text(),
            "password_rules": CustomPasswordValidator().get_help_text(),
            "name_rules": CustomNameValidator().get_help_text(),
            "description_rules": CustomDescriptionValidator().get_help_text(),
            "location_rules": CustomLocationValidator().get_help_text(),
        })
