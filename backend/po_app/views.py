from rest_framework import viewsets, permissions
from rest_framework.response import Response
import requests
from po_app.models import Users, Activities, Allergens, UserActivities, UserAllergens, PlannedActivities
from po_app.serializers import UsersSerializer, ActivitiesSerializer, AllergensSerializer, UserActivitiesSerializer, UserAllergensSerializer, PlannedActivitiesSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users.
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def list(self, request):
        try:
            users = self.queryset
            serializer = UsersSerializer(users, many=True)
            if serializer:
                return Response(serializer.data, status=200)
            return Response(serializer.error_messages, status=400)
        except Exception as e:
            return Response(str(e), status=500)

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
