from rest_framework import viewsets, status
from .permissions import CustomPerm1
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from po_app.models import (
    Users,
    Activities,
    Allergens,
    UserActivities,
    UserAllergens,
    PlannedActivities,
)
from po_app.serializers import (
    UsersSerializer,
    ActivitiesSerializer,
    AllergensSerializer,
    UserActivitiesSerializer,
    UserAllergensSerializer,
    PlannedActivitiesSerializer,
)


class CustomViewset(viewsets.ModelViewSet):
    """
    Custom viewset to manage actions in viewsets.
    """
    hidden_actions = []

    def get_serializer_class(self):
        """
        Modify serializer class based on action.
        """
        if self.action in self.hidden_actions:
            return None
        return super().get_serializer_class()

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch method to exclude hidden actions.
        """
        for action in self.hidden_actions:
            setattr(self, action, self.hidden_action)
        return super().dispatch(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def hidden_action(self, request, *args, **kwargs):
        pass


class UsersViewSet(CustomViewset):
    """
    API endpoint for users.
    """

    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [CustomPerm1]
    hidden_actions = ["update"]

    def list(self, request):
        """
        List all users.
        Special permissions for staff users.
        """
        try:
            users = self.queryset
            serializer = UsersSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """
        Create a new user.
        """
        try:
            serializer = UsersSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """
        Retrieve a user by id.
        Special permissions for staff users.
        """
        try:
            user = self.queryset.get(pk=pk)
            serializer = UsersSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        """
        Update a user by id.
        Special permissions for staff users.
        Special permissions for owner users.
        """
        try:
            user = self.queryset.get(pk=pk)
            serializer = UsersSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        """
        Destroy a user by id.
        Special permissions for staff users.
        Special permissions for owner users.
        """
        try:
            user = self.queryset.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ActivitiesViewSet(viewsets.ModelViewSet):
    """
    API endpoint for activities.
    """

    queryset = Activities.objects.all()
    serializer_class = ActivitiesSerializer

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class AllergensViewSet(viewsets.ModelViewSet):
    """
    API endpoint for allergens.
    """

    queryset = Allergens.objects.all()
    serializer_class = AllergensSerializer

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class UserActivitiesViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user activities.
    """

    queryset = UserActivities.objects.all()
    serializer_class = UserActivitiesSerializer

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class UserAllergensViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user allergens.
    """

    queryset = UserAllergens.objects.all()
    serializer_class = UserAllergensSerializer

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class PlannedActivitiesViewSet(viewsets.ModelViewSet):
    """
    API endpoint for planned activities.
    """

    queryset = PlannedActivities.objects.all()
    serializer_class = PlannedActivitiesSerializer

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
