from rest_framework.permissions import (
    BasePermission,
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)


class CustomPerm1(BasePermission):
    """
    Custom permission class for UsersViewSet
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated or is a staff member
        """
        if view.action in ["list", "retrieve"]:
            return request.user and request.user.is_staff
        elif view.action in ["partial_update", "destroy"]:
            return request.user and (
                request.user.is_authenticated or request.user.is_staff
            )
        elif view.action == "create":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the object or is a staff member
        """
        if view.action in ["retrieve", "partial_update", "destroy"]:
            return request.user and (request.user.is_staff or request.user == obj)
        return False
