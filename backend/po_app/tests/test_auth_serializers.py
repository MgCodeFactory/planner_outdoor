from django.test import TestCase
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from po_app.auth_serializers import (
    CustomPasswordResetSerializer,
    CustomPasswordResetConfirmSerializer,
)
from po_app.models import Users
import os


class CustomPasswordResetSerializerTests(TestCase):
    """
    Tests for CustomPasswordResetSerializer.
    """

    def setUp(self):
        """
        Set up data for tests.
        """
        # valid user data
        self.valid_username = "testuser"
        self.valid_email = "testuser@example.com"
        self.valid_password = os.environ.get("VALID_PASSWORD")
        self.valid_location = {
            "name": "London",
            "lat": 51.5073219,
            "lon": -0.1276474,
            "country": "GB",
        }
        # create a user instance
        self.valid_user = Users.objects.create_user(
            username=self.valid_username,
            email=self.valid_email,
            password=self.valid_password,
            location=self.valid_location,
        )
        self.valid_user.save()

    def test_valid_email_user(self):
        """
        Test that the serializer is valid with a valid email.
        """
        data = {"email": self.valid_email}
        serializer = CustomPasswordResetSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email_user(self):
        """
        Test that the serializer is invalid with an invalid email.
        """
        serializer = CustomPasswordResetSerializer(
            data={"email": "not an email"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)


class CustomPasswordResetConfirmSerializerTests(TestCase):
    """
    Tests for CustomPasswordResetConfirmSerializer.
    """

    def setUp(self):
        """
        Set up data for tests.
        """
        # valid user data
        self.valid_username = "testuser"
        self.valid_email = "testuser@example.com"
        self.valid_password = os.environ.get("VALID_PASSWORD")
        self.new_valid_password = os.environ.get("NEW_VALID_PASSWORD")
        self.valid_location = {
            "name": "London",
            "lat": 51.5073219,
            "lon": -0.1276474,
            "country": "GB",
        }
        # create a user instance
        self.valid_user = Users.objects.create_user(
            username=self.valid_username,
            email=self.valid_email,
            password=self.valid_password,
            location=self.valid_location,
        )
        self.uid = urlsafe_base64_encode(force_bytes(self.valid_user.pk))
        self.token = PasswordResetTokenGenerator().make_token(self.valid_user)
        self.context = {"kwargs": {"uid": self.uid, "token": self.token}}

    def test_valid_password_reset(self):
        """
        Test successful password reset.
        """
        data = {"new_password": self.new_valid_password,
                "confirm_password": self.new_valid_password}
        serializer = CustomPasswordResetConfirmSerializer(
            data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        serializer.validate(data)
        self.valid_user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.new_valid_password))

    def test_password_mismatch(self):
        """
        Test that validation fails when passwords don't match.
        """
        data = {"new_password": self.new_valid_password,
                "confirm_password": "differentpassword"}
        serializer = CustomPasswordResetConfirmSerializer(
            data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_invalid_token(self):
        """
        Test that validation fails with an invalid token.
        """
        self.context["kwargs"]["token"] = "invalid-token"
        data = {"new_password": self.new_valid_password,
                "confirm_password": self.new_valid_password}
        serializer = CustomPasswordResetConfirmSerializer(
            data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
