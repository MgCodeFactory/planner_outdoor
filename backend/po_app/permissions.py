from rest_framework.permissions import BasePermission


class CustomPermUsers(BasePermission):
    """
    Custom permission class for UsersViewSet:
    - Anyone can create an account.
    - User with an account can view/update/delete is own account.
    - Staff can access all accounts.
    """

    def has_permission(self, request, view):
        """
        Manage permissions.
        """
        if view.action == "create":
            return True
        if view.action in ["list", "retrieve"]:
            return request.user and request.user.is_staff
        if view.action in ["partial_update", "destroy"]:
            return request.user and request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, obj):
        """
        Manage object permissions (used after has_permission).
        """
        if view.action in ["retrieve", "partial_update", "destroy"]:
            return request.user and (request.user.is_staff or request.user == obj)
        return False


class CustomPermActivities(BasePermission):
    """
    Custom permission class for Activities and Allergens viewset:
    - User with an account can list Activities and Allergens.
    - Staff can create/update/delete Activities and Allergens.
    """

    def has_permission(self, request, view):
        """
        Manage permissions.
        """
        if view.action == "list":
            return request.user and (
                request.user.is_authenticated or request.user.is_staff
            )
        elif view.action in ["create", "retrieve", "partial_update", "destroy"]:
            return request.user and request.user.is_staff
        return False


class CustomPermPlanned(BasePermission):
    """
    Custom permission class for:
    - UserActivitiesViewSet.
    - UserAllergensViewset.
    - PlannedActivitiesViewset.
    - User with an account manage is own list.
    - Staff can manage all.
    """

    def has_permission(self, request, view):
        """
        Manage permissions.
        """
        if view.action in ["list", "create", "retrieve", "update", "destroy"]:
            return request.user and (
                request.user.is_authenticated or request.user.is_staff
            )
        return False

    def has_object_permission(self, request, view, obj):
        """
        Manage object permissions (used after has_permission).
        """
        if view.action in ["list", "create", "retrieve", "update", "destroy"]:
            return request.user and (request.user.is_staff or request.user == obj)
        return False
