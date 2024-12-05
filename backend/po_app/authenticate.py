from dj_rest_auth.views import UserDetailsView
from .serializers import UsersSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class CustomUserDetailsView(UserDetailsView):
    """
    Overrides the default UserDetailsView to use the UsersSerializer
    Use only GET and PATCH requests (ignore PUT)
    """

    serializer_class = UsersSerializer
    http_method_names = ["get", "patch"]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="username",
                required=True,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="email",
                required=True,
                type=OpenApiTypes.EMAIL,
            ),
            OpenApiParameter(
                name="address",
                required=True,
                type=OpenApiTypes.STR,
            ),
        ],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
