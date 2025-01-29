from django.db import IntegrityError
from django.test import TestCase
from ...models import (
    Users,
    Allergens,
    UserAllergens,
)
import os


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
            location={
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
            },
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
        with self.assertRaises(IntegrityError):
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
            location={
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
            },
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


Exception
