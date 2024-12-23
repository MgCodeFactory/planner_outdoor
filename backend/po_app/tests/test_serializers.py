# from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta
import os
from ..serializers import (
    UsersSerializer,
    ActivitiesSerializer,
    AllergensSerializer,
    UserActivitiesSerializer,
    UserAllergensSerializer,
    PlannedActivitiesSerializer,
)
from ..models import (
    Users,
    Activities,
    Allergens,
    UserActivities,
    UserAllergens,
    PlannedActivities,
)


class UsersSerializerApiTestCase(APITestCase):
    """
    Tests case for the UsersSerializer.
    """

    def setUp(self):
        """
        Set up data for UsersSerializer.
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
            "state": "England",
        }
        # invalid user data
        self.invalid_username = 1234
        self.invalid_email = "not an email"
        self.invalid_password = os.environ.get("INVALID_PASSWORD_TYPE")
        self.invalid_location = "This is not a JSON"
        # data of valid user
        self.valid_user = {
            "username": self.valid_username,
            "email": self.valid_email,
            "password": self.valid_password,
            "location": self.valid_location,
        }
        # create a user instance

        # data of invalid user
        self.invalid_user = {
            "username": self.invalid_username,
            "email": self.invalid_email,
            "password": self.invalid_password,
            "location": self.invalid_location,
        }

    def test_user_valid_data_deserialization(self):
        """
        Test deserialization valid data to user model instance.
        """
        serializer = UsersSerializer(data=self.valid_user)
        self.assertTrue(serializer.is_valid())
        self.assertEqual({}, serializer.errors)

    def test_user_invalid_data_deserialization(self):
        """
        Test deserialization invalid data to user model instance.
        """
        serializer = UsersSerializer(data=self.invalid_user)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)
        self.assertIn("email", serializer.errors)
        self.assertIn("password", serializer.errors)
        self.assertIn("location", serializer.errors)

    def test_user_valid_serialization(self):
        """
        Test deserialization of user instance.
        """
        user = Users.objects.create_user(**self.valid_user)
        serializer = UsersSerializer(user)
        self.assertEqual(
            serializer.data["username"], self.valid_user["username"])
        self.assertEqual(serializer.data["email"], self.valid_user["email"])
        self.assertNotIn("password", serializer.data)
        self.assertEqual(
            serializer.data["location"], self.valid_user["location"])

    def test_create_user_with_serialiser(self):
        """
        Test creating a valid user with serializer.
        """
        user_data = {
            "username": "new_testuser",
            "email": "new_testuser@example.com",
            "password": self.valid_password,
            "location": self.valid_location,
        }
        serializer = UsersSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsInstance(user, Users)
        self.assertEqual(user.username, user_data["username"])
        self.assertEqual(user.email, user_data["email"])
        self.assertTrue(user.check_password(self.valid_user["password"]))
        self.assertEqual(user.location, self.valid_user["location"])


class ActivitiesSerializerApiTestCase(APITestCase):
    """
    Tests case for ActivitiesSerialiser.
    """

    def setUp(self):
        """
        Set up data for ActivitiesSerializer.
        """
        # valid activity data
        self.valid_name = "test activity"
        self.valid_description = "test activity description"
        # invalid activity data
        self.invalid_name = 1234
        self.invalid_description = 1234
        # data for valid activity
        self.valid_activity = {
            "name": self.valid_name,
            "description": self.valid_description,
        }
        # data for invalid activity
        self.invalid_activity = {
            "name": self.invalid_name,
            "description": self.invalid_description,
        }

    def test_activity_valid_data_deserialization(self):
        """
        Test deserialization valid data to activity model instance.
        """
        serializer = ActivitiesSerializer(data=self.valid_activity)
        self.assertTrue(serializer.is_valid())
        self.assertEqual({}, serializer.errors)

    def test_activity_invalid_data_deserialization(self):
        """
        Test deserialization invalid data to activity model instance.
        """
        serializer = ActivitiesSerializer(data=self.invalid_activity)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertIn("description", serializer.errors)

    def test_activity_valid_serialization(self):
        """
        Test deserialization of activity instance.
        """
        activity = Activities.objects.create(**self.valid_activity)
        serializer = ActivitiesSerializer(activity)
        self.assertEqual(serializer.data["name"], self.valid_activity["name"])
        self.assertEqual(
            serializer.data["description"], self.valid_activity["description"]
        )

    def test_create_activity_with_serialiser(self):
        """
        Test creating a valid activity with serializer.
        """
        activity_data = {
            "name": "new test activity",
            "description": "new test activity description",
        }
        serializer = ActivitiesSerializer(data=activity_data)
        self.assertTrue(serializer.is_valid())
        activity = serializer.save()
        self.assertIsInstance(activity, Activities)
        self.assertEqual(activity.name, activity_data["name"])
        self.assertEqual(activity.description, activity_data["description"])


class AllergensSerializerApiTestCase(APITestCase):
    """
    Tests case for AllergensSerialiser.
    """

    def setUp(self):
        """
        Set up data for AllergensSerializer.
        """
        # valid allergen data
        self.valid_name = "test allergen"
        self.valid_description = "test allergen description"
        # invalid allergen data
        self.invalid_name = 1234
        self.invalid_description = 1234
        # data for valid allergen
        self.valid_allergen = {
            "name": self.valid_name,
            "description": self.valid_description,
        }
        # data for invalid allergen
        self.invalid_allergen = {
            "name": self.invalid_name,
            "description": self.invalid_description,
        }

    def test_allergen_valid_data_deserialization(self):
        """
        Test deserialization valid data to allergen model instance.
        """
        serializer = AllergensSerializer(data=self.valid_allergen)
        self.assertTrue(serializer.is_valid())
        self.assertEqual({}, serializer.errors)

    def test_allergen_invalid_data_deserialization(self):
        """
        Test deserialization invalid data to allergen model instance.
        """
        serializer = AllergensSerializer(data=self.invalid_allergen)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertIn("description", serializer.errors)

    def test_allergen_valid_serialization(self):
        """
        Test deserialization of allergen instance.
        """
        allergen = Allergens.objects.create(**self.valid_allergen)
        serializer = AllergensSerializer(allergen)
        self.assertEqual(serializer.data["name"], self.valid_allergen["name"])
        self.assertEqual(
            serializer.data["description"], self.valid_allergen["description"]
        )

    def test_create_allergen_with_serialiser(self):
        """
        Test creating a valid allergen with serializer.
        """
        allergen_data = {
            "name": "new test allergen",
            "description": "new test allergen description",
        }
        serializer = AllergensSerializer(data=allergen_data)
        self.assertTrue(serializer.is_valid())
        allergen = serializer.save()
        self.assertIsInstance(allergen, Allergens)
        self.assertEqual(allergen.name, allergen_data["name"])
        self.assertEqual(allergen.description, allergen_data["description"])


class UserActivitiesSerializerApiTestCase(APITestCase):
    """
    Tests case for UserActivitiesSerialiser.
    """

    def setUp(self):
        """
        Set up data for UserActivitiesSerializer.
        """
        # instance user
        self.user = Users.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password=os.environ.get("VALID_PASSWORD"),
            location={
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
                "state": "England",
            },
        )
        # instance activity
        self.activity = Activities.objects.create(
            name="test activity", description="test activity description"
        )
        # valid user activity data
        self.valid_user = self.user.id
        self.valid_activity = self.activity.id
        # invalid user activity data
        self.invalid_user = "not an integer"
        self.invalid_activity = "not an integer"
        # data for valid user activity
        self.valid_user_activity = {
            "user": self.valid_user,
            "activity": self.valid_activity,
        }
        # data for invalid user activity
        self.invalid_user_activity = {
            "user": self.invalid_user,
            "activity": self.invalid_activity,
        }
        self.bad_user = {
            "user": 999,
            "activity": self.valid_activity,
        }
        self.bad_activity = {
            "user": self.valid_user,
            "activity": 999,
        }

    def test_user_activities_valid_data_deserialization(self):
        """
        Test deserialization valid data to user_activities model instance.
        """
        serializer = UserActivitiesSerializer(data=self.valid_user_activity)
        self.assertTrue(serializer.is_valid())
        self.assertEqual({}, serializer.errors)

    def test_user_activities_invalid_data_deserialization(self):
        """
        Test deserialization invalid data to user_activities model instance.
        """
        serializer = UserActivitiesSerializer(data=self.invalid_user_activity)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)
        self.assertIn("activity", serializer.errors)

    def test_user_activities_valid_serialization(self):
        """
        Test deserialization of user_activities instance.
        """
        user_activity = UserActivities.objects.create(
            user=self.user, activity=self.activity
        )
        serializer = UserActivitiesSerializer(user_activity)
        self.assertEqual(serializer.data["user"], self.user.id)
        self.assertEqual(serializer.data["activity"], self.activity.id)

    def test_user_activities_bad_user(self):
        """
        Test deserialization of user_activities instance with no existing user.
        """
        serializer = UserActivitiesSerializer(data=self.bad_user)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)

    def test_user_activities_bad_activity(self):
        """
        Test deserialization of user_activities instance with no existing activity.
        """
        serializer = UserActivitiesSerializer(data=self.bad_activity)
        self.assertFalse(serializer.is_valid())
        self.assertIn("activity", serializer.errors)


class UserAllergensSerializerApiTestCase(APITestCase):
    """
    Tests case for UserAllergensSerialiser.
    """

    def setUp(self):
        """
        Set up data for UserAllergensSerializer.
        """
        # instance user
        self.user = Users.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password=os.environ.get("VALID_PASSWORD"),
            location={
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
                "state": "England",
            },
        )
        # instance allergen
        self.allergen = Allergens.objects.create(
            name="test allergen", description="test allergen description"
        )
        # valid user allergen data
        self.valid_user = self.user.id
        self.valid_allergen = self.allergen.id
        # invalid user allergen data
        self.invalid_user = "not an integer"
        self.invalid_allergen = "not an integer"
        # data for valid user allergen
        self.valid_user_allergen = {
            "user": self.valid_user,
            "allergen": self.valid_allergen,
        }
        # data for invalid user allergen
        self.invalid_user_allergen = {
            "user": self.invalid_user,
            "allergen": self.invalid_allergen,
        }
        self.bad_user = {
            "user": 999,
            "allergen": self.valid_allergen,
        }
        self.bad_allergen = {
            "user": self.valid_user,
            "allergen": 999,
        }

    def test_user_allergens_valid_data_deserialization(self):
        """
        Test deserialization valid data to user_allergens model instance.
        """
        serializer = UserAllergensSerializer(data=self.valid_user_allergen)
        self.assertTrue(serializer.is_valid())
        self.assertEqual({}, serializer.errors)

    def test_user_allergens_invalid_data_deserialization(self):
        """
        Test deserialization invalid data to user_allergens model instance.
        """
        serializer = UserAllergensSerializer(data=self.invalid_user_allergen)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)
        self.assertIn("allergen", serializer.errors)

    def test_user_allergens_valid_serialization(self):
        """
        Test deserialization of user_allergens instance.
        """
        user_allergen = UserAllergens.objects.create(
            user=self.user, allergen=self.allergen
        )
        serializer = UserAllergensSerializer(user_allergen)
        self.assertEqual(serializer.data["user"], self.user.id)
        self.assertEqual(serializer.data["allergen"], self.allergen.id)

    def test_user_allergens_bad_user(self):
        """
        Test deserialization of user_allergens instance with no existing user.
        """
        serializer = UserAllergensSerializer(data=self.bad_user)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)

    def test_user_allergens_bad_allergen(self):
        """
        Test deserialization of user_allergens instance with no existing allergen.
        """
        serializer = UserAllergensSerializer(data=self.bad_allergen)
        self.assertFalse(serializer.is_valid())
        self.assertIn("allergen", serializer.errors)


class PlannedActivitiesSerializerApiTestCase(APITestCase):
    """
    Tests case for PlannedActivitiesSerialiser.
    """

    def setUp(self):
        """
        Set up data for PlannedActivitiesSerializer.
        """
        # instance user
        self.user = Users.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password=os.environ.get("VALID_PASSWORD"),
            location={
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
                "state": "England",
            },
        )
        # instance activity
        self.activity = Activities.objects.create(
            name="test activity", description="test activity description"
        )
        # data for valid location
        self.valid_location = {
            "name": "London",
            "lat": 51.5073219,
            "lon": -0.1276474,
            "country": "GB",
            "state": "England",
        }
        # data for invalid location
        self.invalid_location = {
            "name": 123,
            "lat": "not a float",
            "lon": "not a float",
            "country": "bad country code",
            "state": 123,
        }
        # valid start_datetime
        self.valid_start_datetime = timezone.now() + timedelta(minutes=30)
        # invalid start_datetime
        self.invalid_start_datetime = "not a datetime"
        # valid end_datetime
        self.valid_end_datetime = timezone.now() + timezone.timedelta(hours=1)
        # invalid end_datetime
        self.invalid_end_datetime = "not a datetime"
        self.invalid_end_datetime_before_start = (
            self.valid_start_datetime - timezone.timedelta(hours=1)
        )
        # data for valid planned_activity
        self.valid_planned_activity = {
            "user": self.user.id,
            "activity": self.activity.id,
            "location": self.valid_location,
            "start_datetime": self.valid_start_datetime,
            "end_datetime": self.valid_end_datetime,
        }
        # data for invalid planned_activity
        self.invalid_planned_activity = {
            "user": self.user.id,
            "activity": self.activity.id,
            "location": self.invalid_location,
            "start_datetime": self.invalid_start_datetime,
            "end_datetime": self.invalid_end_datetime,
        }

    def test_planned_activities_valid_data_deserialization(self):
        """
        Test deserialization valid data to planned_activities model instance.
        """
        serializer = PlannedActivitiesSerializer(
            data=self.valid_planned_activity)
        self.assertTrue(serializer.is_valid())
        self.assertEqual({}, serializer.errors)

    def tes_planned_activities_invalid_data_deserialization(self):
        """
        Test deserialization invalid data to planned_activities model instance.
        """
        serializer = PlannedActivitiesSerializer(
            data=self.invalid_planned_activity)
        self.assertFalse(serializer.is_valid())
        self.assertIn("location", serializer.errors)
        self.assertIn("start_datetime", serializer.errors)
        self.assertIn("end_datetime", serializer.errors)

    def test_planned_activities_valid_serialization(self):
        """
        Test deserialization of planned_activities instance.
        """
        planned_activity = PlannedActivities.objects.create(
            user=self.user,
            activity=self.activity,
            location=self.valid_location,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        serializer = PlannedActivitiesSerializer(planned_activity)
        self.assertEqual(serializer.data["user"], self.user.id)
        self.assertEqual(serializer.data["activity"], self.activity.id)
        self.assertEqual(serializer.data["location"], self.valid_location)
        self.assertEqual(
            serializer.data["start_datetime"],
            self.valid_start_datetime.isoformat().replace("+00:00", "Z"),
        )
        self.assertEqual(
            serializer.data["end_datetime"],
            self.valid_end_datetime.isoformat().replace("+00:00", "Z"),
        )

    def test_create_planned_activity_with_serializer(self):
        """
        Test creating a planned activity with the serializer.
        """
        serializer = PlannedActivitiesSerializer(
            data=self.valid_planned_activity)
        self.assertTrue(serializer.is_valid())
        planned_activity = serializer.save()
        self.assertIsInstance(planned_activity, PlannedActivities)
        self.assertEqual(planned_activity.user, self.user)
        self.assertEqual(planned_activity.activity, self.activity)
        self.assertEqual(planned_activity.location, self.valid_location)
        self.assertEqual(planned_activity.start_datetime,
                         self.valid_start_datetime)
        self.assertEqual(planned_activity.end_datetime,
                         self.valid_end_datetime)
