from django.db import IntegrityError
from django.test import TestCase
from ...models import (
    Users,
    Activities,
    UserActivities,
)
import os


class UserActivitiesTestCase(TestCase):
    """
    Tests for UserActivities model.
    """

    def setUp(self):
        """
        Set up data for UserActivities model.
        """
        self.user = Users.objects.create_user(
            username="testuser",
            email="test@example.com",
            password=os.environ.get("VALID_PASSWORD"),
            location={
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
            },
        )
        self.activity = Activities.objects.create(
            name="Test Activity", description="This is a test activity description"
        )

    def test_create_valid_user_activity(self):
        """
        Test creating a valid user activity.
        """
        user_activity = UserActivities.objects.create(
            user=self.user,
            activity=self.activity,
        )
        self.assertEqual(user_activity.user_id, self.user.id)
        self.assertEqual(user_activity.activity_id, self.activity.id)
        self.assertIsNotNone(user_activity.id)

    def test_user_activity_relationships(self):
        """
        Test UserActivities model relationship with Users and Activities.
        """
        user_activity = UserActivities.objects.create(
            user=self.user,
            activity=self.activity,
        )
        self.assertEqual(user_activity.user, self.user)
        self.assertEqual(user_activity.activity, self.activity)

    def test_cascade_delete_user(self):
        """
        Test cascade delete when a user is deleted.
        """
        user_activity = UserActivities.objects.create(
            user=self.user,
            activity=self.activity,
        )
        self.user.delete()
        with self.assertRaises(UserActivities.DoesNotExist):
            UserActivities.objects.get(id=user_activity.id)
        self.assertTrue(Activities.objects.filter(
            id=self.activity.id).exists())

    def test_cascade_delete_activity(self):
        """
        Test cascade delete when an activity is deleted.
        """
        user_activity = UserActivities.objects.create(
            user=self.user,
            activity=self.activity,
        )
        self.activity.delete()
        with self.assertRaises(UserActivities.DoesNotExist):
            UserActivities.objects.get(id=user_activity.id)
        self.assertTrue(Users.objects.filter(id=self.user.id).exists())

    def test_user_activity_unique_constraint(self):
        """
        Test unique constraint on user_id and activity_id.
        """
        UserActivities.objects.create(
            user=self.user,
            activity=self.activity,
        )
        with self.assertRaises(IntegrityError):
            UserActivities.objects.create(
                user=self.user,
                activity=self.activity,
            )

    def test_user_with_new_activity(self):
        """
        Test creating a new activity for a user.
        """
        new_activity = Activities.objects.create(
            name="New Activity", description="This is a new activity description"
        )
        user_activity = UserActivities.objects.create(
            user=self.user,
            activity=new_activity,
        )
        self.assertEqual(user_activity.user_id, self.user.id)
        self.assertEqual(user_activity.activity_id, new_activity.id)
        self.assertIsNotNone(user_activity.id)

    def test_activity_with_new_user(self):
        """
        Test creating a new user for an activity.
        """
        new_user = Users.objects.create_user(
            username="new_testuser",
            email="new_testuser@example.com",
            password=os.environ.get("VALID_PASSWORD"),
            location={
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
            },
        )
        user_activity = UserActivities.objects.create(
            user=new_user,
            activity=self.activity,
        )
        self.assertEqual(user_activity.user_id, new_user.id)
        self.assertEqual(user_activity.activity_id, self.activity.id)
        self.assertIsNotNone(user_activity.id)

    def test_user_activity_str_method(self):
        """
        Test the __str__ method of the UserActivities model.
        """
        user_activity = UserActivities.objects.create(
            user=self.user,
            activity=self.activity,
        )
        self.assertEqual(
            str(user_activity),
            f"{
                self.user.username} - {self.activity.name}",
        )
