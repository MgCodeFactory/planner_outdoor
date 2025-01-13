from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ...models import Users
import os


class UsersViewsetTest(APITestCase):
    """
    Test class for Users viewset.
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

    def test_users_list_unauthenticated(self):
        """
        Test that unauthenticated users can't access users list.
        """
        url = reverse("users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_list_authenticated(self):
        """
        Test that authenticated users can't access users list.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_list_staff(self):
        """
        Test that staff users can access users list.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_user(self):
        """
        Test that anyone can create a new user.
        """
        url = reverse("users-list")
        data = {
            "username": "create_new_user",
            "email": "create_new_user@example.com",
            "password": os.environ.get("VALID_PASSWORD"),
            "location": {
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
                "state": "England",
            },
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Users.objects.count(), 4)
        self.assertEqual(response.data["username"], "create_new_user")

    def test_create_user_invalid_data(self):
        """
        Test it's not possible to create user with invalid data.
        """
        url = reverse("users-list")
        data = {
            "username": 123,
            "email": "test_create_user@example.com",
            "password": os.environ.get("VALID_PASSWORD"),
            "location": {
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
                "state": "England",
            },
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Users.objects.count(), 3)

    def test_users_retreive_unauthenticated(self):
        """
        Test that unauthenticated users can't access user details.
        """
        url = reverse("user-detail", kwargs={"pk": self.unauth_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_retrieve_authenticated(self):
        """
        Test that authenticated users can't access other user details.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-detail", kwargs={"pk": self.unauth_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_retreive_authenticated_owner(self):
        """
        Test that authenticated users can access their own user details.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-detail", kwargs={"pk": self.auth_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.auth_user.username)

    def test_users_retreive_staff(self):
        """
        Test that staff users can access all user details.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("user-detail", kwargs={"pk": self.auth_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.auth_user.username)
        url = reverse("user-detail", kwargs={"pk": self.unauth_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.unauth_user.username)

    def test_users_partial_update_unauthenticated(self):
        """
        Test that unauthenticated users can't update user details.
        """
        url = reverse("user-detail", kwargs={"pk": self.unauth_user.pk})
        response = self.client.patch(url, {"username": "updated_unauth_user"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_partial_update_authenticated(self):
        """
        Test that authenticated users can't update other user details.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-detail", kwargs={"pk": self.unauth_user.pk})
        response = self.client.patch(url, {"username": "updated_unauth_user"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_partial_update_authenticated_owner(self):
        """
        Test that authenticated users can update their own user details.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-detail", kwargs={"pk": self.auth_user.pk})
        response = self.client.patch(url, {"username": "updated_auth_user"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "updated_auth_user")

    def test_users_partial_update_staff(self):
        """
        Test that staff users can update all user details.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("user-detail", kwargs={"pk": self.auth_user.pk})
        response = self.client.patch(url, {"username": "updated_auth_user"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "updated_auth_user")
        url = reverse("user-detail", kwargs={"pk": self.unauth_user.pk})
        response = self.client.patch(url, {"username": "updated_unauth_user"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "updated_unauth_user")

    def test_users_destroy_unauthenticated(self):
        """
        Test that unauthenticated users can't delete user.
        """
        url = reverse("user-detail", kwargs={"pk": self.unauth_user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_destroy_authenticated(self):
        """
        Test that authenticated users can't delete other user.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-detail", kwargs={"pk": self.unauth_user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_destroy_authenticated_owner(self):
        """
        Test that authenticated users can delete their own user.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-detail", kwargs={"pk": self.auth_user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Users.objects.count(), 2)

    def test_users_destroy_staff(self):
        """
        Test that staff users can delete all user.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("user-detail", kwargs={"pk": self.auth_user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Users.objects.count(), 2)
        url = reverse("user-detail", kwargs={"pk": self.unauth_user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Users.objects.count(), 1)
