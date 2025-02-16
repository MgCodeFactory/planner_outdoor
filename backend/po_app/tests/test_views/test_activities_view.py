from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ...models import Users, Activities
import os


class ActivitiesViewsetTest(APITestCase):
    """
    Test class for Activities viewset.
    """

    def setUp(self):
        # instance unauthenticated user
        self.unauth_user = Users.objects.create_user(
            username="test_unauth_user",
            email="test_unauth_user@example.com",
            password=os.environ.get("VALID_PASSWORD"),
            location={
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
            },
        )
        # instance authenticated user
        self.auth_user = Users.objects.create_user(
            username="test_auth_user",
            email="test_auth_user@example.com",
            password=os.environ.get("VALID_PASSWORD"),
            location={
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
            },
        )
        # instance staff user
        self.staff_user = Users.objects.create_user(
            username="test_staff_user",
            email="test_staff_user@example.com",
            password=os.environ.get("VALID_PASSWORD"),
            location={
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
            },
            is_staff=True,
        )
        # instance for Activities
        self.activity_1 = Activities.objects.create(
            name="testactivity 1",
            description="test activity description 1",
        )
        self.activity_2 = Activities.objects.create(
            name="testactivity 2",
            description="test activity description 2",
        )
        self.activity_3 = Activities.objects.create(
            name="testactivity 3",
            description="test activity description 3",
        )

    def test_activities_list_unauthenticated(self):
        """
        Test that unauthenticated users can't access activities list.
        """
        url = reverse("activities-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_activities_list_authenticated(self):
        """
        Test that authenticated users can access activities list.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("activities-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activities_list_staff(self):
        """
        Test that staff users can access activities list.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("activities-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_activity_unauthenticated(self):
        """
        Test that unauthenticated users can't create a new activity.
        """
        url = reverse("activities-list")
        data = {
            "name": "testactivity 4",
            "description": "test activity description 4",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Activities.objects.count(), 3)

    def test_create_activity_authenticated(self):
        """
        Test that authenticated users can't create a new activity.
        """
        url = reverse("activities-list")
        data = {"name": "testactivity 4",
                "description": "test activity description 4"}
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Activities.objects.count(), 3)

    def test_create_activity_staff(self):
        """
        Test that staff users can create a new activity.
        """
        url = reverse("activities-list")
        data = {
            "name": "testactivity 4",
            "description": "test activity description 4",
        }
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activities.objects.count(), 4)
        self.assertEqual(response.data["name"], "testactivity 4")

    def test_create_activity_invalid_data(self):
        """
        Test it's not possible to create an activity with invalid data.
        """
        url = reverse("activities-list")
        data = {
            "name": 123,
            "description": "test activity description 5",
        }
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Activities.objects.count(), 3)

    def test_activity_retreive_unauthenticated(self):
        """
        Test that unauthenticated users can't access activity details.
        """
        url = reverse("activity-detail", kwargs={"pk": self.activity_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_activity_retrieve_authenticated(self):
        """
        Test that authenticated users can't access activity details.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("activity-detail", kwargs={"pk": self.activity_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_activity_retreive_staff(self):
        """
        Test that staff users can access all activities details.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("activity-detail", kwargs={"pk": self.activity_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse("activity-detail", kwargs={"pk": self.activity_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activity_partial_update_unauthenticated(self):
        """
        Test that unauthenticated users can't update activity details.
        """
        url = reverse("activity-detail", kwargs={"pk": self.activity_2.id})
        response = self.client.patch(url, {"name": "new activity name"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_partial_update_authenticated(self):
        """
        Test that authenticated users can't update activity details.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("activity-detail", kwargs={"pk": self.activity_3.id})
        response = self.client.patch(
            url, {"description": "new activity description"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_activity_partial_update_staff(self):
        """
        Test that staff users can update all activity details.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("activity-detail", kwargs={"pk": self.activity_1.id})
        response = self.client.patch(url, {"name": "updated activity name 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "updated activity name 1")
        url = reverse("activity-detail", kwargs={"pk": self.activity_3.id})
        response = self.client.patch(
            url, {"description": "updated activity description 3"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"],
                         "updated activity description 3")

    def test_activity_partial_update_duplicated_values(self):
        """
        Test it's not possible to update an activity with duplicated values.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("activity-detail", kwargs={"pk": self.activity_1.id})
        response = self.client.patch(url, {"name": "testactivity 2"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.patch(
            url, {"description": "test activity description 2"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_users_destroy_unauthenticated(self):
        """
        Test that unauthenticated users can't delete activity.
        """
        url = reverse("activity-detail", kwargs={"pk": self.activity_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_activity_destroy_authenticated(self):
        """
        Test that authenticated users can't delete activity.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("activity-detail", kwargs={"pk": self.activity_2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_activity_destroy_staff(self):
        """
        Test that staff users can delete all activities.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("activity-detail", kwargs={"pk": self.activity_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Activities.objects.count(), 2)
        url = reverse("activity-detail", kwargs={"pk": self.activity_2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Activities.objects.count(), 1)
