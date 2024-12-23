from .test_models_common import BaseNameDescriptionTestCase
from django.db import IntegrityError
from ...models import Activities


class ActivitiesTestCase(BaseNameDescriptionTestCase):
    """
    Tests for Activities model.
    """

    def test_create_valid_activity(self):
        """
        Test creating a valid activity.
        """
        Activities.objects.create(
            name=self.valid_activity_name,
            description=self.valid_activity_description,
        )
        self.assertTrue(Activities.objects.get(name=self.valid_activity_name))
        self.assertTrue(
            Activities.objects.get(description=self.valid_activity_description)
        )

    def test_name_activity_uniqueness(self):
        """
        Test activity name uniqueness.
        """
        Activities.objects.create(
            name=self.valid_activity_name,
            description=self.valid_activity_description,
        )
        with self.assertRaises(IntegrityError):
            Activities.objects.create(
                name=self.existing_activity_name,
                description="This is a new activity description.",
            )
            self.assertFalse(Activities.objects.get(
                name=self.valid_activity_name))

    def test_activity_description_uniqueness(self):
        """
        Test activity description uniqueness.
        """
        Activities.objects.create(
            name=self.valid_activity_name,
            description=self.valid_activity_description,
        )
        with self.assertRaises(IntegrityError):
            Activities.objects.create(
                name="New activity name.",
                description=self.existing_activity_description,
            )
            self.assertFalse(
                Activities.objects.get(
                    description=self.valid_activity_description)
            )

    def test_activities_str_method(self):
        """
        Test the __str__ method for the Activities model.
        """
        activity = Activities.objects.create(
            name=self.valid_activity_name,
            description=self.valid_activity_description,
        )
        self.assertEqual(
            str(activity),
            f"{
                activity.name} - {activity.description}",
        )
