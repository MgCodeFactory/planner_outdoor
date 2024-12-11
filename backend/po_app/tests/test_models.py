from django.test import TestCase
from ..models import (
    Users,
    Activities,
    Allergens,
    UserActivities,
    UserAllergens,
    PlannedActivities,
)
from ..validators import CustomPasswordValidator
from django.utils import timezone
from datetime import timedelta
import random
import string
import os


class UsersTestCase(TestCase):
    """
    Tests for Users model.
    """

    def setUp(self):
        """
        Set up the test data for Users model.
        """
        # data for username
        self.valid_username = "testuser"
        for i in range(51):
            self.invalid_useranme_len = "".join(
                random.choices(string.ascii_letters, k=i)
            )
        self.invalid_username_type = 123
        self.invalid_username_null = ""
        self.invalid_username_blank = " "
        self.existing_username = self.valid_username
        self.invalid_username_bad_special = "testuser#"
        # data for password
        self.valid_password = os.environ.get("VALID_PASSWORD")
        self.invalid_password_len = os.environ.get("INVALID_PASSWORD_LEN")
        self.invalid_password_type = os.environ.get("INVALID_PASSWORD_TYPE")
        self.invalid_password_no_upper = os.environ.get(
            "INVALID_PASSWORD_NO_UPPER")
        self.invalid_password_no_lower = os.environ.get(
            "INVALID_PASSWORD_NO_LOWER")
        self.invalid_password_no_digit = os.environ.get(
            "INVALID_PASSWORD_NO_DIGIT")
        self.invalid_password_no_special = os.environ.get(
            "INVALID_PASSWORD_NO_SPECIAL")
        self.invalid_password_no_diff = os.environ.get(
            "INVALID_PASSWORD_NO_DIFF")
        self.invalid_password_null = ""
        self.invalid_password_blank = " "
        # data for email
        self.valid_email = "test@example.com"
        self.invalid_email = "invalid_email"
        self.existing_email = self.valid_email
        self.invalid_email_type = 123
        self.invalid_email_null = ""
        self.invalid_email_blank = " "
        # data for address
        self.valid_address = "Paris"
        for i in range(201):
            self.invalid_address_len = "".join(
                random.choices(string.ascii_letters, k=i)
            )
        self.invalid_address_type = 123
        self.invalid_address_null = ""
        self.invalid_address_blank = " "

    def test_valid_password(self):
        """
        Test valid password.
        """
        validator = CustomPasswordValidator()
        validator.validate(self.valid_password)

    def test_invalid_password(self):
        """
        Test invalid password using CustomPasswordValidator.
        """
        invalid_passwords = (
            self.invalid_password_len,
            self.invalid_password_type,
            self.invalid_password_no_upper,
            self.invalid_password_no_lower,
            self.invalid_password_no_digit,
            self.invalid_password_no_special,
            self.invalid_password_no_diff,
            self.invalid_password_null,
            self.invalid_password_blank,
        )
        validator = CustomPasswordValidator()
        with self.assertRaises(Exception):
            for password in invalid_passwords:
                validator.validate(password)

    def test_create_valid_user(self):
        """
        Test creating a valid user.
        """
        user = Users.objects.create_user(
            username=self.valid_username,
            email=self.valid_email,
            password=self.valid_password,
            address=self.valid_address,
        )
        self.assertEqual(user.username, self.valid_username)
        self.assertEqual(user.email, self.valid_email)
        self.assertTrue(user.check_password(self.valid_password))
        self.assertEqual(user.address, self.valid_address)

    def test_invalid_username(self):
        """
        Test creating a user with invalid username.
        """
        invalid_usernames = (
            self.invalid_useranme_len,
            self.invalid_username_type,
            self.invalid_username_null,
            self.invalid_username_blank,
            self.existing_username,
            self.invalid_username_bad_special,
        )
        for username in invalid_usernames:
            with self.assertRaises(Exception):
                user = Users.objects.create_user(
                    username=username,
                    email=self.valid_email,
                    password=self.valid_password,
                    address=self.valid_address,
                )
                self.assertFalse(user.username, username)
                self.assertEqual(user.email, self.valid_email)
                self.assertTrue(user.check_password(self.valid_password))
                self.assertEqual(user.address, self.valid_address)

    def test_invalid_email(self):
        """
        Test creating a user with invalid email.
        """
        invalid_emails = (
            self.invalid_email,
            self.invalid_email_type,
            self.invalid_email_null,
            self.invalid_email_blank,
            self.existing_email,
        )
        for email in invalid_emails:
            with self.assertRaises(Exception):
                user = Users.objects.create_user(
                    username=self.valid_username,
                    email=email,
                    password=self.valid_password,
                    address=self.valid_address,
                )
                self.assertEqual(user.username, self.valid_username)
                self.assertFalse(user.email, email)
                self.assertTrue(user.check_password(self.valid_password))
                self.assertEqual(user.address, self.valid_address)

    def test_invalid_address(self):
        """
        Test creating a user with invalid address.
        """
        invalid_addresses = (
            self.invalid_address_len,
            self.invalid_address_type,
            self.invalid_address_null,
            self.invalid_address_blank,
        )
        for address in invalid_addresses:
            with self.assertRaises(Exception):
                user = Users.objects.create_user(
                    username=self.valid_username,
                    email=self.valid_email,
                    password=self.valid_password,
                    address=address,
                )
                self.assertEqual(user.username, self.valid_username)
                self.assertEqual(user.email, self.valid_email)
                self.assertTrue(user.check_password(self.valid_password))
                self.assertFalse(user.address, address)

    def test_existing_usermame(self):
        """
        Test creating a user with an existing username.
        """
        user = Users.objects.create_user(
            username=self.valid_username,
            email=self.valid_email,
            password=self.valid_password,
            address=self.valid_address,
        )

        with self.assertRaises(Exception):
            new_user = Users.objects.create_user(
                username=user.username,
                email="new_test@example.com",
                password=self.valid_password,
                address=self.valid_address,
            )
            self.assertEqual(new_user.username, user.username)
            self.assertEqual(new_user.email, "new_test@example.com")
            self.assertTrue(new_user.check_password(self.valid_password))
            self.assertEqual(new_user.address, self.valid_address)

    def test_existing_email(self):
        """
        Test creating a user with an existing email.
        """
        user = Users.objects.create_user(
            username=self.valid_username,
            email=self.valid_email,
            password=self.valid_password,
            address=self.valid_address,
        )
        with self.assertRaises(Exception):
            new_user = Users.objects.create_user(
                username="new testuser",
                email=user.email,
                password=self.valid_password,
                address=self.valid_address,
            )
            self.assertEqual(new_user.username, "new testuser")
            self.assertEqual(new_user.email, user.email)
            self.assertTrue(user.check_password(self.valid_password))
            self.assertEqual(user.address, self.valid_address)

    def test_users_str_method(self):
        """
        Test the __str__ method of the Users model.
        """
        user = Users.objects.create_user(
            username=self.valid_username,
            email=self.valid_email,
            password=self.valid_password,
            address=self.valid_address,
        )
        self.assertEqual(str(user), f"{user.username} - {user.email}")


class ActivitiesTestCase(TestCase):
    """
    Tests for Activities model.
    """

    def setUp(self):
        """
        Set up data for Activities model.
        """
        # data for name
        self.valid_name = "Test Activity"
        for i in range(51):
            self.invalid_name_len = "".join(
                random.choices(string.ascii_letters, k=i))
        self.existing_name = self.valid_name
        self.invalid_name_type = 123
        self.invalid_name_null = ""
        self.invalid_name_blank = " "
        # data for description
        self.valid_description = "This is a test activity description"
        for i in range(201):
            self.invalid_description_len = "".join(
                random.choices(string.ascii_letters, k=i)
            )
        self.invalid_description_type = 123
        self.invalid_description_null = ""
        self.invalid_description_blank = " "

    def test_create_valid_activity(self):
        """
        Test creating a valid activity.
        """
        activity = Activities.objects.create(
            name=self.valid_name, description=self.valid_description
        )
        self.assertEqual(activity.name, self.valid_name)
        self.assertEqual(activity.description, self.valid_description)

    def test_invalid_name(self):
        """
        Test creating an activity with invalid name.
        """
        invalid_names = (
            self.invalid_name_len,
            self.invalid_name_type,
            self.invalid_name_null,
            self.invalid_name_blank,
            self.existing_name,
        )
        for name in invalid_names:
            with self.assertRaises(Exception):
                activity = Activities.objects.create(
                    name=name, description=self.valid_description
                )
                self.assertFalse(activity.name, name)
                self.assertEqual(activity.description, self.valid_description)

    def test_invalid_description(self):
        """
        Test creating an activity with invalid description.
        """
        invalid_descriptions = (
            self.invalid_description_len,
            self.invalid_description_type,
            self.invalid_description_null,
            self.invalid_description_blank,
        )
        for description in invalid_descriptions:
            with self.assertRaises(Exception):
                activity = Activities.objects.create(
                    name=self.valid_name, description=description
                )
                self.assertEqual(activity.name, self.valid_name)
                self.assertFalse(activity.description, description)

    def test_activities_str_method(self):
        """
        Test the __str__ method of the Activities model.
        """
        activity = Activities.objects.create(
            name=self.valid_name, description=self.valid_description
        )
        self.assertEqual(
            str(activity),
            f"{
                activity.name} - {activity.description}",
        )


class AllergensTestCase(TestCase):
    """
    Tests for Allergens model.
    """

    def setUp(self):
        """
        Set up data for Allergens model.
        """
        # data for name
        self.valid_name = "Test Allergen"
        for i in range(51):
            self.invalid_name_len = "".join(
                random.choices(string.ascii_letters, k=i))
        self.existing_name = self.valid_name
        self.invalid_name_type = 123
        self.invalid_name_null = ""
        self.invalid_name_blank = " "
        # data for description
        self.valid_description = "This is a test allergen description"
        for i in range(201):
            self.invalid_description_len = "".join(
                random.choices(string.ascii_letters, k=i)
            )
        self.invalid_description_type = 123
        self.invalid_description_null = ""
        self.invalid_description_blank = " "

    def test_create_valid_allergen(self):
        """
        Test creating a valid allergen.
        """
        allergen = Allergens.objects.create(
            name=self.valid_name, description=self.valid_description
        )
        self.assertEqual(allergen.name, self.valid_name)
        self.assertEqual(allergen.description, self.valid_description)

    def test_invalid_name(self):
        """
        Test creating an allergen with invalid name.
        """
        invalid_names = (
            self.invalid_name_len,
            self.invalid_name_type,
            self.invalid_name_null,
            self.invalid_name_blank,
            self.existing_name,
        )
        for name in invalid_names:
            with self.assertRaises(Exception):
                allergen = Allergens.objects.create(
                    name=name, description=self.valid_description
                )
                self.assertFalse(allergen.name, name)
                self.assertEqual(allergen.description, self.valid_description)

    def test_invalid_description(self):
        """
        Test creating an allergen with invalid description.
        """
        invalid_descriptions = (
            self.invalid_description_len,
            self.invalid_description_type,
            self.invalid_description_null,
            self.invalid_description_blank,
        )
        for description in invalid_descriptions:
            with self.assertRaises(Exception):
                allergen = Allergens.objects.create(
                    name=self.valid_name, description=description
                )
                self.assertEqual(allergen.name, self.valid_name)
                self.assertFalse(allergen.description, description)

    def test_allergens_str_method(self):
        """
        Test the __str__ method of the Allergens model.
        """
        allergen = Allergens.objects.create(
            name=self.valid_name, description=self.valid_description
        )
        self.assertEqual(
            str(allergen),
            f"{
                allergen.name} - {allergen.description}",
        )


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
        with self.assertRaises(Exception):
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
            f"{self.user.username} - {self.activity.name}",
        )


class UserAllergensTestCase(TestCase):
    """
    Tests for UserAllergens model.
    """

    def setUp(self):
        """
        Set up data for UserAllergens model.
        """
        self.user = Users.objects.create_user(
            username="testuser",
            email="test@example.com",
            password=os.environ.get("VALID_PASSWORD"),
        )
        self.allergen = Allergens.objects.create(
            name="Test Allergen", description="This is a test allergen description"
        )

    def test_create_valid_user_allergen(self):
        """
        Test creating a valid user allergen.
        """
        user_allergen = UserAllergens.objects.create(
            user=self.user,
            allergen=self.allergen,
        )
        self.assertEqual(user_allergen.user_id, self.user.id)
        self.assertEqual(user_allergen.allergen_id, self.allergen.id)
        self.assertIsNotNone(user_allergen.id)

    def test_user_allergen_relationships(self):
        """
        Test UserAllergens model relationship with Users and Activities.
        """
        user_allergen = UserAllergens.objects.create(
            user=self.user,
            allergen=self.allergen,
        )
        self.assertEqual(user_allergen.user, self.user)
        self.assertEqual(user_allergen.allergen, self.allergen)

    def test_cascade_delete_user(self):
        """
        Test cascade delete when a user is deleted.
        """
        user_allergen = UserAllergens.objects.create(
            user=self.user,
            allergen=self.allergen,
        )
        self.user.delete()
        with self.assertRaises(UserAllergens.DoesNotExist):
            UserAllergens.objects.get(id=user_allergen.id)
        self.assertTrue(Allergens.objects.filter(id=self.allergen.id).exists())

    def test_cascade_delete_allergen(self):
        """
        Test cascade delete when an allergen is deleted.
        """
        user_allergen = UserAllergens.objects.create(
            user=self.user,
            allergen=self.allergen,
        )
        self.allergen.delete()
        with self.assertRaises(UserAllergens.DoesNotExist):
            UserAllergens.objects.get(id=user_allergen.id)
        self.assertTrue(Users.objects.filter(id=self.user.id).exists())

    def test_user_allergen_unique_constraint(self):
        """
        Test unique constraint on user_id and allergen_id.
        """
        UserAllergens.objects.create(
            user=self.user,
            allergen=self.allergen,
        )
        with self.assertRaises(Exception):
            UserAllergens.objects.create(
                user=self.user,
                allergen=self.allergen,
            )

    def test_user_with_new_allergen(self):
        """
        Test creating a new allergen for a user.
        """
        new_allergen = Allergens.objects.create(
            name="New allergen", description="This is a new allergen description"
        )
        user_allergen = UserAllergens.objects.create(
            user=self.user,
            allergen=new_allergen,
        )
        self.assertEqual(user_allergen.user_id, self.user.id)
        self.assertEqual(user_allergen.allergen_id, new_allergen.id)
        self.assertIsNotNone(user_allergen.id)

    def test_allergen_with_new_user(self):
        """
        Test creating a new user for an allergen.
        """
        new_user = Users.objects.create_user(
            username="new_testuser",
            email="new_testuser@example.com",
            password=os.environ.get("VALID_PASSWORD"),
        )
        user_allergen = UserAllergens.objects.create(
            user=new_user,
            allergen=self.allergen,
        )
        self.assertEqual(user_allergen.user_id, new_user.id)
        self.assertEqual(user_allergen.allergen_id, self.allergen.id)
        self.assertIsNotNone(user_allergen.id)

    def test_user_allergen_str_method(self):
        """
        Test the __str__ method of the UserAllergens model.
        """
        user_allergen = UserAllergens.objects.create(
            user=self.user,
            allergen=self.allergen,
        )
        self.assertEqual(
            str(user_allergen),
            f"{self.user.username} - {self.allergen.name}",
        )


class PlannedActivitiesTestCase(TestCase):
    """
    Test for PlannedActivities model.
    """

    def setUp(self):
        """
        Set up data for PlannedActivities model.
        """
        self.user = Users.objects.create_user(
            username="testuser",
            email="test@example.com",
            password=os.environ.get("VALID_PASSWORD"),
        )
        self.activity = Activities.objects.create(
            name="Test Activity", description="This is a test activity description"
        )
        # data for location
        self.valid_location = "This is a test location"
        self.invalid_location_type = 123
        self.invalid_location_null = ""
        self.invalid_location_blank = "   "
        for i in range(201):
            self.invalid_location_len = "".join(
                random.choices(string.ascii_letters, k=i)
            )
        # data for start_datetime and end_datetime
        self.valid_start_datetime = timezone.now()
        self.invalid_start_datetime_type = "not a datetime"
        self.invalid_start_datetime_null = ""
        self.invalid_start_datetime_blank = "   "
        self.invalid_start_datetime_past = timezone.now() - timedelta(hours=2)
        self.valid_end_datetime = self.valid_start_datetime + \
            timedelta(hours=2)
        self.invalid_end_datetime_type = "not a datetime"
        self.invalid_end_datetime_null = ""
        self.invalid_end_datetime_blank = "   "

    def test_planned_activity_invalid_location(self):
        """
        Test creating planned activities with invalid location.
        """
        invalid_locations = (
            self.invalid_location_type,
            self.invalid_location_null,
            self.invalid_location_blank,
            self.invalid_location_len,
        )
        for location in invalid_locations:
            with self.assertRaises(Exception):
                planned_activity = PlannedActivities.objects.create(
                    user=self.user,
                    activity=self.activity,
                    location=location,
                    start_datetime=self.valid_start_datetime,
                    end_datetime=self.valid_end_datetime,
                )
                self.assertEqual(planned_activity.user_id, self.user.id)
                self.assertEqual(planned_activity.activity_id,
                                 self.activity.id)
                self.assertFalse(planned_activity.location, location)
                self.assertEqual(planned_activity.start_datetime,
                                 self.valid_start_datetime)
                self.assertEqual(planned_activity.end_datetime,
                                 self.valid_end_datetime)

    def test_planned_activity_invalid_start_datetime(self):
        """
        Test creating planned activities with invalid start_datetime.
        """
        invalid_start_datetimes = (
            self.invalid_start_datetime_type,
            self.invalid_start_datetime_null,
            self.invalid_start_datetime_blank,
            self.invalid_start_datetime_past,
        )
        for datetime in invalid_start_datetimes:
            with self.assertRaises(Exception):
                planned_activity = PlannedActivities.objects.create(
                    user=self.user,
                    activity=self.activity,
                    location=self.valid_location,
                    start_datetime=datetime,
                    end_datetime=self.valid_end_datetime,
                )
                self.assertEqual(planned_activity.user_id, self.user.id)
                self.assertEqual(planned_activity.activity_id,
                                 self.activity.id)
                self.assertEqual(planned_activity.location,
                                 self.valid_location)
                self.assertFalse(planned_activity.start_datetime, datetime)
                self.assertEqual(planned_activity.end_datetime,
                                 self.valid_end_datetime)

    def test_planned_activity_invalid_end_datetime(self):
        """
        Test creating planned activities with invalid end_datetime.
        """
        invalid_end_datetimes = (
            self.invalid_end_datetime_type,
            self.invalid_end_datetime_null,
            self.invalid_end_datetime_blank,
        )
        for datetime in invalid_end_datetimes:
            with self.assertRaises(Exception):
                planned_activity = PlannedActivities.objects.create(
                    user=self.user,
                    activity=self.activity,
                    location=self.valid_location,
                    start_datetime=self.valid_start_datetime,
                    end_datetime=datetime,
                )
                self.assertEqual(planned_activity.user_id, self.user.id)
                self.assertEqual(planned_activity.activity_id,
                                 self.activity.id)
                self.assertEqual(planned_activity.location,
                                 self.valid_location)
                self.assertEqual(planned_activity.start_datetime,
                                 self.valid_start_datetime)
                self.assertFalse(planned_activity.end_datetime, datetime)

    def test_create_valid_planned_activity(self):
        """
        Test creating a valid planned activity.
        """
        planned_activity = PlannedActivities.objects.create(
            user=self.user,
            activity=self.activity,
            location=self.valid_location,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        self.assertEqual(planned_activity.user_id, self.user.id)
        self.assertEqual(planned_activity.activity_id, self.activity.id)
        self.assertEqual(planned_activity.location, self.valid_location)
        self.assertEqual(planned_activity.start_datetime,
                         self.valid_start_datetime)
        self.assertEqual(planned_activity.end_datetime,
                         self.valid_end_datetime)
        self.assertIsNotNone(planned_activity.id)

    def test_planned_activity_relationships(self):
        """
        Test PlannedActivities model relationship with Users and Activities.
        """
        planned_activity = PlannedActivities.objects.create(
            user=self.user,
            activity=self.activity,
            location=self.valid_location,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        self.assertEqual(planned_activity.user, self.user)
        self.assertEqual(planned_activity.activity, self.activity)

    def test_cascade_delete_user(self):
        """
        Test cascade delete when a user is deleted.
        """
        planned_activity = PlannedActivities.objects.create(
            user=self.user,
            activity=self.activity,
            location=self.valid_location,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        self.user.delete()
        with self.assertRaises(PlannedActivities.DoesNotExist):
            PlannedActivities.objects.get(id=planned_activity.id)
        self.assertTrue(Activities.objects.filter(
            id=self.activity.id).exists())

    def test_cascade_delete_activity(self):
        """
        Test cascade delete when an activity is deleted.
        """
        planned_activity = PlannedActivities.objects.create(
            user=self.user,
            activity=self.activity,
            location=self.valid_location,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        self.activity.delete()
        with self.assertRaises(PlannedActivities.DoesNotExist):
            PlannedActivities.objects.get(id=planned_activity.id)
        self.assertTrue(Users.objects.filter(id=self.user.id).exists())

    def test_planned_activity_unique_constraint(self):
        """
        Test unique constraint on user, activity, start_datetime, end_datetime.
        """
        PlannedActivities.objects.create(
            user=self.user,
            activity=self.activity,
            location=self.valid_location,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        with self.assertRaises(Exception):
            PlannedActivities.objects.create(
                user=self.user,
                activity=self.activity,
                location="This is a new location test",
                start_datetime=self.valid_start_datetime,
                end_datetime=self.valid_end_datetime,
            )

    def test_same_planned_activity_with_new_datetime(self):
        """
        Test creating a new planned activity with the same user, activity, and location.
        """
        planned_activity = PlannedActivities.objects.create(
            user=self.user,
            activity=self.activity,
            location=self.valid_location,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        new_planned_activity = PlannedActivities.objects.create(
            user=self.user,
            activity=self.activity,
            location=self.valid_location,
            start_datetime=self.valid_start_datetime + timedelta(hours=2),
            end_datetime=self.valid_end_datetime + timedelta(hours=2),
        )
        self.assertEqual(new_planned_activity.user_id,
                         planned_activity.user_id)
        self.assertEqual(new_planned_activity.activity_id,
                         planned_activity.activity_id)
        self.assertEqual(new_planned_activity.location,
                         planned_activity.location)
        self.assertIsNotNone(new_planned_activity.id)

    def test_same_planned_activity_with_new_user(self):
        """
        Test creating a new planned activity with the same activity, location, and datetime.
        """
        planned_activity = PlannedActivities.objects.create(
            user=self.user,
            activity=self.activity,
            location=self.valid_location,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        new_user = Users.objects.create_user(
            username="new_testuser",
            email="new_testuser@example.com",
            password=os.environ.get("VALID_PASSWORD"),
        )
        new_planned_activity = PlannedActivities.objects.create(
            user=new_user,
            activity=self.activity,
            location=self.valid_location,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        self.assertEqual(new_planned_activity.user_id, new_user.id)
        self.assertEqual(new_planned_activity.activity_id,
                         planned_activity.activity_id)
        self.assertEqual(new_planned_activity.location,
                         planned_activity.location)
        self.assertIsNotNone(new_planned_activity.id)

    def test_planned_activity_with_new_activity(self):
        """
        Test creating a new planned activity with the same user, location, and datetime.
        """
        planned_activity = PlannedActivities.objects.create(
            user=self.user,
            activity=self.activity,
            location=self.valid_location,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        new_activity = Activities.objects.create(
            name="New Test Activity",
            description="This is a new test activity description",
        )
        new_planned_activity = PlannedActivities.objects.create(
            user=self.user,
            activity=new_activity,
            location=self.valid_location,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        self.assertEqual(new_planned_activity.user_id,
                         planned_activity.user_id)
        self.assertEqual(new_planned_activity.activity_id, new_activity.id)
        self.assertEqual(new_planned_activity.location,
                         planned_activity.location)
        self.assertIsNotNone(new_planned_activity.id)

    def test_planned_activity_str_method(self):
        """
        Test the __str__ method of the PlannedActivities model.
        """
        planned_activity = PlannedActivities.objects.create(
            user=self.user,
            activity=self.activity,
            location=self.valid_location,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        expected_str = f"{planned_activity.user.username} - {planned_activity.activity.name} - {
            planned_activity.start_datetime} - {planned_activity.end_datetime}"
        self.assertEqual(str(planned_activity), expected_str)
