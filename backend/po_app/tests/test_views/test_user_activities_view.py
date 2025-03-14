from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ...models import Users, Activities, UserActivities
import os


class UserActivitiesViewsetTest(APITestCase):
    """
    Test class for User Activities viewset.
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
        self.activity_4 = Activities.objects.create(
            name="testactivity 4",
            description="test activity description 4",
        )
        # instance for UserActivities
        self.user_activity_1 = UserActivities.objects.create(
            user=self.auth_user, activity=self.activity_1
        )
        self.user_activity_2 = UserActivities.objects.create(
            user=self.auth_user, activity=self.activity_2
        )
        self.user_activity_3 = UserActivities.objects.create(
            user=self.staff_user, activity=self.activity_3
        )

    def test_user_activities_list_unauthenticated(self):
        """
        Test that unauthenticated users can't access user activities list.
        """
        url = reverse("user-activities-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_activities_list_authenticated_owner(self):
        """
        Test that authenticated users can onlly access his own activities list.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-activities-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertNotEqual(len(response.data), 3)

    def test_user_activities_list_staff(self):
        """
        Test that staff users can access user activities list.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("user-activities-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_user_activity_unauthenticated(self):
        """
        Test that unauthenticated users can't create a new user activity.
        """
        url = reverse("user-activities-list")
        data = {"user": self.unauth_user.id, "activity": self.activity_1.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(UserActivities.objects.count(), 3)

    def test_create_user_activity_authenticated(self):
        """
        Test that authenticated users can create a new user activity.
        """
        url = reverse("user-activities-list")
        data = {"user": self.auth_user.id, "activity": self.activity_4.id}
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserActivities.objects.filter(
            user=self.auth_user).count(), 3)

    def test_create_activity_staff(self):
        """
        Test that staff users can create a new user activity.
        """
        url = reverse("user-activities-list")
        data = {"user": self.staff_user.id, "activity": self.activity_1.id}
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserActivities.objects.count(), 4)

    def test_create_user_activity_invalid_data(self):
        """
        Test it's not possible to create a user activity with invalid data.
        """
        url = reverse("user-activities-list")
        data = {"user": "invalid_user", "activity": self.activity_1.id}
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserActivities.objects.count(), 3)

    def test_user_activity_retreive_unauthenticated(self):
        """
        Test that unauthenticated users can't access user activity.
        """
        url = reverse("user-activity-detail",
                      kwargs={"pk": self.user_activity_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_activity_retrieve_authenticated_owner(self):
        """
        Test that authenticated user can access only is own activity.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-activity-detail",
                      kwargs={"pk": self.user_activity_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse("user-activity-detail",
                      kwargs={"pk": self.user_activity_3.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_activity_retreive_staff(self):
        """
        Test that staff users can access all users activities.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("user-activity-detail",
                      kwargs={"pk": self.user_activity_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse("user-activity-detail",
                      kwargs={"pk": self.user_activity_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_activity_update_unauthenticated(self):
        """
        Test that unauthenticated users can't update user activity.
        """
        url = reverse("user-activity-detail",
                      kwargs={"pk": self.user_activity_2.id})
        response = self.client.put(
            url, {"user": self.staff_user.id, "activity": self.activity_2.id}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_activity_update_authenticated_owner(self):
        """
        Test that authenticated user can update his own activity.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-activity-detail",
                      kwargs={"pk": self.user_activity_1.id})
        response = self.client.put(
            url, {"user": self.auth_user.id, "activity": self.activity_4.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_activity_update_authenticated_not_owner(self):
        """
        Test that authenticated user can't update another user activity.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-activity-detail",
                      kwargs={"pk": self.user_activity_3.id})
        response = self.client.put(
            url, {"user": self.auth_user.id, "activity": self.activity_4.id}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_activity_update_staff(self):
        """
        Test that staff users can update all users activities.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("user-activity-detail",
                      kwargs={"pk": self.user_activity_1.id})
        response = self.client.put(
            url, {"user": self.auth_user.id, "activity": self.activity_4.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_activity_updated = UserActivities.objects.get(
            id=self.user_activity_1.id)
        self.assertEqual(user_activity_updated.activity.name,
                         self.activity_4.name)
        url = reverse("user-activity-detail",
                      kwargs={"pk": self.user_activity_2.id})
        response = self.client.put(
            url, {"user": self.staff_user.id, "activity": self.activity_1.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_activity_updated = UserActivities.objects.get(
            id=self.user_activity_2.id)
        self.assertEqual(user_activity_updated.user, self.staff_user)

    def test_user_activity_destroy_unauthenticated(self):
        """
        Test that unauthenticated users can't delete a user activity.
        """
        url = reverse("user-activity-detail",
                      kwargs={"pk": self.user_activity_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_activity_destroy_authenticated_owner(self):
        """
        Test that authenticated user can only delete his own activity.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-activity-detail",
                      kwargs={"pk": self.user_activity_2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_activity_destroy_authenticated_not_owner(self):
        """
        Test that authenticated user can't delete other user activity.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-activity-detail",
                      kwargs={"pk": self.user_activity_3.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_activity_destroy_staff(self):
        """
        Test that staff users can delete all user activities.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("user-activity-detail",
                      kwargs={"pk": self.user_activity_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserActivities.objects.count(), 2)
        url = reverse("user-activity-detail",
                      kwargs={"pk": self.user_activity_2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserActivities.objects.count(), 1)
