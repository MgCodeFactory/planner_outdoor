from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta
from .test_models_common import BaseLocationTestCase
from ...validators import CustomLocationValidator
from ...models import (
    Users,
    Activities,
    PlannedActivities,
)


class PlannedActivitiesTestCase(BaseLocationTestCase):
    """
    Test for PlannedActivities model.
    """

    def setUp(self):
        """
        Set up data for PlannedActivities model.
        """
        super().setUp()
        # instance user and activity for PlannedActivities:42:39
        self.user = Users.objects.create_user(
            username="user for planned_activity",
            email="user.planned@example.com",
            password=self.valid_password,
            location=self.valid_location,
        )
        self.activity = Activities.objects.create(
            name="Planned activity", description="test planned_activity description"
        )
        # data for start_datetime and end_datetime
        self.valid_start_datetime = timezone.now() + timedelta(minutes=30)
        self.valid_end_datetime = self.valid_start_datetime + \
            timedelta(hours=2)
        self.invalid_start_datetime_type = "not a datetime"
        self.invalid_start_datetime_null = ""
        self.invalid_start_datetime_blank = "   "
        self.invalid_start_datetime_before_now = self.valid_start_datetime - \
            timedelta(hours=4)
        self.invalid_end_datetime_before_start = self.valid_start_datetime - \
            timedelta(hours=2)
        self.invalid_end_datetime_type = "not a datetime"
        self.invalid_end_datetime_null = ""
        self.invalid_end_datetime_blank = "   "

    def test_location_null(self):
        """
        Test planned activity location null value.
        """
        planned_activity = PlannedActivities(
            user=self.user,
            activity=self.activity,
            location=self.invalid_location_null,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        with self.assertRaises(ValidationError):
            planned_activity.full_clean()
            CustomLocationValidator()(planned_activity.location)

    def test_location_blank(self):
        """
        Test planned activity location blank value.
        """
        planned_activity = PlannedActivities(
            user=self.user,
            activity=self.activity,
            location=self.invalid_location_blank,
            start_datetime=self.valid_start_datetime,
            end_datetime=self.valid_end_datetime,
        )
        with self.assertRaises(ValidationError):
            planned_activity.full_clean()
            CustomLocationValidator()(planned_activity.location)

    def test_invalid_start_datetime_type(self):
        """,
        Test invalid start_datetime type.
        """
        with self.assertRaises(ValidationError):
            planned_activity = PlannedActivities.objects.create(
                user=self.user,
                activity=self.activity,
                location=self.valid_location,
                start_datetime=self.invalid_start_datetime_type,
                end_datetime=self.valid_end_datetime,
            )
            planned_activity.full_clean()
            self.assertIsNot(isinstance(
                planned_activity.start_datetime, timezone))

    def test_invalid_end_datetime_type(self):
        """,
        Test invalid end_datetime type.
        """
        with self.assertRaises(ValidationError):
            planned_activity = PlannedActivities.objects.create(
                user=self.user,
                activity=self.activity,
                location=self.valid_location,
                start_datetime=self.valid_start_datetime,
                end_datetime=self.invalid_end_datetime_type,
            )
            planned_activity.full_clean()
            self.assertIsNot(isinstance(
                planned_activity.end_datetime, timezone))

    def test_invalid_start_datetime_null(self):
        """
        Test invalid start_datetime null value.
        """
        with self.assertRaises(ValidationError):
            planned_activity = PlannedActivities.objects.create(
                user=self.user,
                activity=self.activity,
                location=self.valid_location,
                start_datetime=self.invalid_start_datetime_null,
                end_datetime=self.valid_end_datetime,
            )
            planned_activity.full_clean()
            self.assertIsNot(isinstance(
                planned_activity.start_datetime, timezone))

    def test_invalid_end_datetime_null(self):
        """
        Test invalid end_datetime null value.
        """
        with self.assertRaises(ValidationError):
            planned_activity = PlannedActivities.objects.create(
                user=self.user,
                activity=self.activity,
                location=self.valid_location,
                start_datetime=self.valid_start_datetime,
                end_datetime=self.invalid_end_datetime_null,
            )
            planned_activity.full_clean()
            self.assertIsNot(isinstance(
                planned_activity.end_datetime, timezone))

    def test_invalid_start_datetime_blank(self):
        """
        Test invalid start_datetime blank value.
        """
        with self.assertRaises(ValidationError):
            planned_activity = PlannedActivities.objects.create(
                user=self.user,
                activity=self.activity,
                location=self.valid_location,
                start_datetime=self.invalid_start_datetime_blank,
                end_datetime=self.valid_end_datetime,
            )
            planned_activity.full_clean()
            self.assertIsNot(isinstance(
                planned_activity.start_datetime, timezone))

    def test_invalid_end_datetime_blank(self):
        """
        Test invalid end_datetime blank value.
        """
        with self.assertRaises(ValidationError):
            planned_activity = PlannedActivities.objects.create(
                user=self.user,
                activity=self.activity,
                location=self.valid_location,
                start_datetime=self.valid_start_datetime,
                end_datetime=self.invalid_end_datetime_blank,
            )
            planned_activity.full_clean()
            self.assertIsNot(isinstance(
                planned_activity.end_datetime, timezone))

    def test_invalid_start_datetime_before_now(self):
        """
        Test invalid start_datetime before now.
        """
        with self.assertRaises(ValidationError):
            planned_activity = PlannedActivities.objects.create(
                user=self.user,
                activity=self.activity,
                location=self.valid_location,
                start_datetime=self.invalid_start_datetime_before_now,
                end_datetime=self.valid_end_datetime,
            )
            planned_activity.full_clean()
            self.assertTrue(planned_activity.start_datetime <
                            self.valid_start_datetime)

    def test_invalid_end_datetime_before_start(self):
        """
        Test invalid end_datetime before start.
        """
        with self.assertRaises(ValidationError):
            planned_activity = PlannedActivities.objects.create(
                user=self.user,
                activity=self.activity,
                location=self.valid_location,
                start_datetime=self.valid_start_datetime,
                end_datetime=self.invalid_end_datetime_before_start,
            )
            planned_activity.full_clean()
            self.assertTrue(planned_activity.end_datetime <
                            self.valid_start_datetime)

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
        with self.assertRaises(IntegrityError):
            PlannedActivities.objects.create(
                user=self.user,
                activity=self.activity,
                location=self.valid_location,
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
            password=self.valid_password,
            location=self.valid_location,
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
