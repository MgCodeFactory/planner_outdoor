from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ...models import Users, Activities, PlannedActivities
from django.utils import timezone
from datetime import timedelta
import os


class PlannedActivitiesViewsetTest(APITestCase):
    """
    Test class for Planned Activities viewset.
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
                "state": "England",
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
                "state": "England",
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
                "state": "England",
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
        self.activity_4 = Activities.objects.create(
            name="testactivity 4",
            description="test activity description 4",
        )
        self.activity_5 = Activities.objects.create(
            name="testactivity 5",
            description="test activity description 5",
        )
        self.activity_6 = Activities.objects.create(
            name="testactivity 6",
            description="test activity description 6",
        )
        # data for location
        self.location_1 = {
            "name": "London",
            "lat": 51.5073219,
            "lon": -0.1276474,
            "country": "GB",
            "state": "England",
        }
        self.location_2 = {
            "name": "London",
            "lat": 51.5073219,
            "lon": -0.1276474,
            "country": "GB",
            "state": "England",
        }
        self.location_3 = {
            "name": "Rome",
            "lat": 41.902782,
            "lon": 12.496366,
            "country": "IT",
            "state": "Lazio",
        }
        # data for start_datetime and end_datetime
        start_datetime = timezone.now() + timedelta(minutes=30)
        self.valid_start_datetime = start_datetime.strftime("%Y-%m-%d %H:%M")
        end_datetime = start_datetime + timedelta(hours=2)
        self.valid_end_datetime = end_datetime.strftime("%Y-%m-%d %H:%M")

        # instance for planned Activities
        self.planned_activity_1 = PlannedActivities.objects.create(
            user=self.auth_user,
            activity=self.activity_1,
            location=self.location_1,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        self.planned_activity_2 = PlannedActivities.objects.create(
            user=self.auth_user,
            activity=self.activity_2,
            location=self.location_2,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        self.planned_activity_3 = PlannedActivities.objects.create(
            user=self.staff_user,
            activity=self.activity_3,
            location=self.location_3,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )

    def test_planned_activities_list_unauthenticated(self):
        """
        Test that unauthenticated users can't access user planned activities list.
        """
        url = reverse("planned-activities-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_planned_activities_list_authenticated_owner(self):
        """
        Test that authenticated users can only access his own planned activity list.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("planned-activities-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertNotEqual(len(response.data), 3)

    def test_planned_activities_list_staff(self):
        """
        Test that staff users can access all users planned activities list.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("planned-activities-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_planned_activity_unauthenticated(self):
        """
        Test that unauthenticated users can't create a new planned activity.
        """
        url = reverse("planned-activities-list")
        data = {
            "user": self.unauth_user.id,
            "activity": self.activity_1.id,
            "location": self.location_1,
            "start_datetime": self.valid_start_datetime,
            "end_datetime": self.valid_end_datetime,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(PlannedActivities.objects.count(), 3)

    def test_create_planned_activity_authenticated(self):
        """
        Test that authenticated users can create a new planned activity.
        """
        url = reverse("planned-activities-list")
        data = {
            "user": self.auth_user.id,
            "activity": self.activity_5.id,
            "location": self.location_3,
            "start_datetime": self.valid_start_datetime,
            "end_datetime": self.valid_end_datetime,
        }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            PlannedActivities.objects.filter(user=self.auth_user).count(), 3
        )

    def test_create_planned_activity_staff(self):
        """
        Test that staff users can create a new planned activity.
        """
        url = reverse("planned-activities-list")
        data = {
            "user": self.staff_user.id,
            "activity": self.activity_6.id,
            "location": self.location_1,
            "start_datetime": self.valid_start_datetime,
            "end_datetime": self.valid_end_datetime,
        }
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PlannedActivities.objects.count(), 4)

    def test_create_planned_activity_invalid_data(self):
        """
        Test it's not possible to create a planned activity with invalid data.
        """
        url = reverse("planned-activities-list")
        data = {
            "user": self.auth_user.id,
            "activity": self.activity_1.id,
            "location": "not a valid location",
            "start_datetime": self.valid_start_datetime,
            "end_datetime": self.valid_end_datetime,
        }
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PlannedActivities.objects.count(), 3)

    def test_planned_activity_retreive_unauthenticated(self):
        """
        Test that unauthenticated users can't access planned activity.
        """
        url = reverse(
            "planned-activity-detail", kwargs={"pk": self.planned_activity_1.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_planned_activity_retrieve_authenticated_owner(self):
        """
        Test that authenticated user can access only is own planned activity.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse(
            "planned-activity-detail", kwargs={"pk": self.planned_activity_2.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse(
            "planned-activity-detail", kwargs={"pk": self.planned_activity_3.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_planned_activity_retreive_staff(self):
        """
        Test that staff users can access all planned activities.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse(
            "planned-activity-detail", kwargs={"pk": self.planned_activity_1.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse(
            "planned-activity-detail", kwargs={"pk": self.planned_activity_2.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_planned_activity_update_unauthenticated(self):
        """
        Test that unauthenticated users can't update a planned activity.
        """
        url = reverse(
            "planned-activity-detail", kwargs={"pk": self.planned_activity_1.id}
        )
        data = {
            "user": self.auth_user.id,
            "activity": self.activity_1.id,
            "location": self.location_3,
            "start_datetime": self.valid_start_datetime,
            "end_datetime": self.valid_end_datetime,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_planned_activity_update_authenticated_owner(self):
        """
        Test that authenticated user can update his own activity.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse(
            "planned-activity-detail", kwargs={"pk": self.planned_activity_1.id}
        )
        data = {
            "user": self.auth_user.id,
            "activity": self.activity_1.id,
            "location": self.location_3,
            "start_datetime": self.valid_start_datetime,
            "end_datetime": self.valid_end_datetime,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_planned_activity_update_authenticated_not_owner(self):
        """
        Test that authenticated user can't update another planned activity.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse(
            "planned-activity-detail", kwargs={"pk": self.planned_activity_3.id}
        )
        data = {
            "user": self.auth_user.id,
            "activity": self.activity_3.id,
            "location": self.location_3,
            "start_datetime": self.valid_start_datetime,
            "end_datetime": self.valid_end_datetime,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_planned_activity_update_staff(self):
        """
        Test that staff users can update all planned activities.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse(
            "planned-activity-detail", kwargs={"pk": self.planned_activity_1.id}
        )
        data = {
            "user": self.staff_user.id,
            "activity": self.activity_1.id,
            "location": self.location_3,
            "start_datetime": self.valid_start_datetime,
            "end_datetime": self.valid_end_datetime,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_activity_updated = PlannedActivities.objects.get(
            id=self.planned_activity_1.id
        )
        self.assertEqual(user_activity_updated.user, self.staff_user)
        url = reverse(
            "planned-activity-detail", kwargs={"pk": self.planned_activity_2.id}
        )
        data = {
            "user": self.staff_user.id,
            "activity": self.activity_2.id,
            "location": self.location_3,
            "start_datetime": self.valid_start_datetime,
            "end_datetime": self.valid_end_datetime,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_activity_updated = PlannedActivities.objects.get(
            id=self.planned_activity_2.id
        )
        self.assertEqual(user_activity_updated.location, self.location_3)

    def test_planned_activity_destroy_unauthenticated(self):
        """
        Test that unauthenticated users can't delete a planned activity.
        """
        url = reverse(
            "planned-activity-detail", kwargs={"pk": self.planned_activity_1.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_planned_activity_destroy_authenticated_owner(self):
        """
        Test that authenticated user can only delete his own planned activity.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse(
            "planned-activity-detail", kwargs={"pk": self.planned_activity_2.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_planned_activity_destroy_authenticated_not_owner(self):
        """
        Test that authenticated user can't delete other user planned activity.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse(
            "planned-activity-detail", kwargs={"pk": self.planned_activity_3.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_planned_activity_destroy_staff(self):
        """
        Test that staff users can delete all user planned activities.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse(
            "planned-activity-detail", kwargs={"pk": self.planned_activity_1.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PlannedActivities.objects.count(), 2)
        url = reverse(
            "planned-activity-detail", kwargs={"pk": self.planned_activity_2.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PlannedActivities.objects.count(), 1)
