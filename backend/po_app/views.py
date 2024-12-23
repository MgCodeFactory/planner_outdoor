from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from .permissions import (
    CustomPermUsers,
    CustomPermActivities,
    CustomPermPlanned,
)
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


"""class CustomViewset(viewsets.ModelViewSet):
    
    Custom viewset to manage actions in viewsets.
    

    def get_schema_operation(self, path, method):
        
        Override the get_schema_operation
        to exclude actions listed in "hidden_actions.
        
        method = method.lower()
        action = self.action_map.get(method, '')

        if action in self.hidden_actions:
            return None
        return super().get_schema_operation(path, method)

    def get_serializer_class(self):
        
        Just return the get_serializer_class
        
        return super().get_serializer_class()

    def dispatch(self, request, *args, **kwargs):
        
        Just return the dispatch method.
        
        return super().dispatch(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def hidden_action(self, request, *args, **kwargs):
        
        Hide method in drf_spectacular documentation.
        
        pass"""


class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users.
    """

    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [CustomPermUsers]

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

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT", detail="Method PUT not allowed.")

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
    permission_classes = [CustomPermActivities]

    def list(self, request):
        """
        List all activities.pass
        Special permissions for staff users.
        """
        try:
            activities = self.queryset
            serializer = ActivitiesSerializer(activities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        raise MethodNotAllowed("PUT", detail="Method PUT not allowed.")

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
    permission_classes = [CustomPermActivities]

    def list(self, request):
        """
        List all Allergens.
        Special permissions for staff users.
        """
        try:
            allergens = self.queryset
            serializer = AllergensSerializer(allergens, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        raise MethodNotAllowed("PUT", detail="Method PUT not allowed.")

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
    permission_classes = [CustomPermPlanned]

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH", detail="Method PATCH not allowed.")

    def destroy(self, request, pk=None):
        pass


class UserAllergensViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user allergens.
    """

    queryset = UserAllergens.objects.all()
    serializer_class = UserAllergensSerializer
    permission_classes = [CustomPermPlanned]

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH", detail="Method PATCH not allowed.")

    def destroy(self, request, pk=None):
        pass


class PlannedActivitiesViewSet(viewsets.ModelViewSet):
    """
    API endpoint for planned activities.
    """

    queryset = PlannedActivities.objects.all()
    serializer_class = PlannedActivitiesSerializer
    permission_classes = [CustomPermPlanned]

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH", detail="Method PATCH not allowed.")

    def destroy(self, request, pk=None):
        pass
