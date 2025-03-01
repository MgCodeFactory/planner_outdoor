from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from po_app.models import (
    Users,
    Activities,
    UserActivities,
    PlannedActivities,
)
from po_app.serializers import (
    UsersSerializer,
    ActivitiesSerializer,
    UserActivitiesSerializer,
    PlannedActivitiesSerializer,
)


class ApiRootView(APIView):
    """
    API root view.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        API root help endpoint.
        """
        return Response({
            "message": "Welcome to Planner outdoor API. For complete documentation visit:",
            "swagger_url": request.build_absolute_uri('/schema/swagger/'),
            "redoc_url": request.build_absolute_uri('/schema/redoc/'),
        })


class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users.
    """

    serializer_class = UsersSerializer

    def get_queryset(self):
        """
        Handle queryset for Users actions.
        """
        if self.action == "create":
            return Users.objects.none()
        elif self.action == "list":
            return Users.objects.all()
        elif self.action in ["retrieve", "partial_update", "destroy"]:
            if self.request.user.is_staff:
                return Users.objects.all()
            return Users.objects.filter(id=self.request.user.id)
        else:
            return Users.objects.none()

    def get_permissions(self):
        """
        Handle permissions for Users actions.
        """
        if self.action == "create":
            permission_classes = [AllowAny]
        elif self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action in ["retrieve", "partial_update", "destroy"]:
            permission_classes = [IsAdminUser | IsAuthenticated]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def list(self, request):
        """
        List all users.
        Special permissions for staff users.
        """
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        Retrieve a user by id.
        Special permissions for staff users.
        """
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT", detail="Method PUT not allowed.")

    def partial_update(self, request, pk=None):
        """
        Update a user by id.
        Special permissions for staff users.
        Special permissions for owner users.
        """
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Destroy a user by id.
        Special permissions for staff users.
        Special permissions for owner users.
        """
        user = self.get_object()
        self.perform_destroy(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivitiesViewSet(viewsets.ModelViewSet):
    """
    API endpoint for activities.
    """

    serializer_class = ActivitiesSerializer

    def get_queryset(self):
        """
        Handle queryset for Activities actions.
        """
        if self.action == "list":
            if self.request.user.is_staff or self.request.user.is_authenticated:
                return Activities.objects.all()
        elif self.action in ["create", "retrieve", "partial_update", "destroy"]:
            if self.request.user.is_staff:
                return Activities.objects.all()
        else:
            return Activities.objects.none()

    def get_permissions(self):
        """
        Handle permissions for Activities actions.
        """
        if self.action == "list":
            permission_classes = [IsAdminUser | IsAuthenticated]
        elif self.action in ["create", "retrieve", "partial_update", "destroy"]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def list(self, request):
        """
        List all activities.
        Special permissions for staff and authenticated users.
        """
        activities = self.get_queryset()
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new activity.
        Special permissions for staff users.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        Retrieve an activity by id.
        Special permissions for staff users.
        """
        activity = self.get_object()
        serializer = self.get_serializer(activity)
        return Response(serializer.data)

    def update(self, request, pk=None):
        raise MethodNotAllowed("PUT", detail="Method PUT not allowed.")

    def partial_update(self, request, pk=None):
        """
        Update an activity by id.
        Special permissions for staff users.
        """
        activity = self.get_object()
        serializer = self.get_serializer(
            activity, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Destroy an activity by id.
        Special permissions for staff users.
        """
        activity = self.get_object()
        self.perform_destroy(activity)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserActivitiesViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user activities.
    """

    serializer_class = UserActivitiesSerializer

    def get_queryset(self):
        """
        Handle queryset for UserActivities actions.
        """
        if self.action in ["list", "create", "retrieve", "update", "destroy"]:
            if self.request.user.is_staff:
                return UserActivities.objects.all()
            return UserActivities.objects.filter(user=self.request.user)
        else:
            return UserActivities.objects.none()

    def get_permissions(self):
        """
        Handle permissions for UserActivities actions.
        """
        if self.action in ["list", "create", "retrieve", "update", "destroy"]:
            permission_classes = [IsAdminUser | IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def list(self, request):
        """
        List all User Activities.
        Special permissions for staff and authenticated users.
        """
        user_activities = self.get_queryset()
        serializer = self.get_serializer(user_activities, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new User Activity.
        Special permissions for staff and authenticated users.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        Retrieve a User Activity by id.
        Special permissions for staff and authenticated users.
        """
        user_activity = self.get_object()
        serializer = self.get_serializer(user_activity)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Update a User Activity by id.
        Special permissions for staff and authenticated users.
        """
        user_activity = self.get_object()
        serializer = self.get_serializer(
            user_activity, data=request.data, partial=False
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH", detail="Method PATCH not allowed.")

    def destroy(self, request, pk=None):
        """
        Destroy a User Activity by id.
        Special permissions for staff and authenticated users.
        """
        user_activity = self.get_object()
        self.perform_destroy(user_activity)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlannedActivitiesViewSet(viewsets.ModelViewSet):
    """
    API endpoint for planned activities.
    """

    serializer_class = PlannedActivitiesSerializer

    def get_queryset(self):
        """
        Handle queryset for PlannedActivities actions.
        """
        if self.action in ["list", "create", "retrieve", "update", "destroy"]:
            if self.request.user.is_staff:
                return PlannedActivities.objects.all()
            return PlannedActivities.objects.filter(user=self.request.user)
        else:
            return PlannedActivities.objects.none()

    def get_permissions(self):
        """
        Handle permissions for PlannedActvities actions.
        """
        if self.action in ["list", "create", "retrieve", "update", "destroy"]:
            permission_classes = [IsAdminUser | IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def list(self, request):
        """
        List all Planned Activities.
        Special permissions for staff and authenticated users.
        """
        planned_activities = self.get_queryset()
        serializer = self.get_serializer(planned_activities, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new Planned Activity.
        Special permissions for staff and authenticated users.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        Retrieve a Planned Activity by id.
        Special permissions for staff and authenticated users.
        """
        planned_activity = self.get_object()
        serializer = self.get_serializer(planned_activity)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Update a Planned Activity by id.
        Special permissions for staff and authenticated users.
        """
        planned_activity = self.get_object()
        serializer = self.get_serializer(
            planned_activity, data=request.data, partial=False
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH", detail="Method PATCH not allowed.")

    def destroy(self, request, pk=None):
        """
        Destroy a Planned Activity by id.
        Special permissions for staff and authenticated users.
        """
        planned_activity = self.get_object()
        self.perform_destroy(planned_activity)
        return Response(status=status.HTTP_204_NO_CONTENT)
