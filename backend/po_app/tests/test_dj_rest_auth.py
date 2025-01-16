from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Users
import os


class DjRestAuthTests(APITestCase):
    """
    class test for the 3rd package dj-rest-auth authentication package.
    """

    def setUp(self):
        # instance authenticated user
        self.plain_password = os.environ.get("VALID_PASSWORD")
        self.auth_user = Users.objects.create_user(
            username="test_auth_user",
            email="test_auth_user@example.com",
            password=self.plain_password,
            location={
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
                "state": "England",
            },
        )

    def test_valid_auth_user_login_with_username(self):
        """
        test login with valid credentials using username.
        """
        url = reverse("rest_login")
        print(f"Login URL: {url}")
        data = {
            "username": self.auth_user.username,
            "password": self.plain_password,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("key" in response.data)

    def test_valid_auth_user_login_with_email(self):
        """
        test login with valid credentials using email.
        """
        url = reverse("rest_login")
        data = {
            "email": self.auth_user.email,
            "password": self.auth_user.password,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("key" in response.data)

    def test_invalid_unauth_user_login(self):
        """
        test login with invalid credentials.
        """
        url = reverse("rest_login")
        data = {
            "username": "wrong username",
            "password": "wrong password"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("non_field_errors" in response.data)

    def test_logout(self):
        """
        test logout.
        """
        url = reverse("rest_logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("detail" in response.data)

    def test_password_reset(self):
        """
        test password reset.
        """
        url = reverse("rest_password_reset")
        data = {"email": self.auth_user.email}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("detail" in response.data)

    def test_password_reset_confirm(self):
        """
        test password reset confirm.
        """
        url = reverse("rest_password_reset_confirm")
        data = {
            "new_password1": os.environ.get("NEW_VALID_PASSWORD"),
            "new_password2": os.environ.get("NEW_VALID_PASSWORD"),
            "uid": self.auth_user.pk,
            "token": "set-password",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("detail" in response.data)

    def test_password_change(self):
        """
        test password change.
        """
        url = reverse("rest_password_change")
        data = {
            "new_password1": os.environ.get("NEW_VALID_PASSWORD"),
            "new_password2": os.environ.get("NEW_VALID_PASSWORD"),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("detail" in response.data)
        self.client.logout()

    def test_user_details_get(self):
        """
        # test user details get.
        """
        url = reverse("rest_user_details")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("username" in response.data)

    def test_user_details_put(self):
        """
        test user details put.
        """
        url = reverse("rest_user_details")
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("username" in response.data)

    def test_user_details_patch(self):
        """
        test user details patch.
        """
        url = reverse("rest_user_details")
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("username" in response.data)
