from .test_models_common import BaseNameDescriptionTestCase
from django.db import IntegrityError
from ...models import Allergens


class AllergensTestCase(BaseNameDescriptionTestCase):
    """
    Tests for Allergens model.
    """

    def test_create_valid_allergen(self):
        """
        Test creating a valid allergen.
        """
        Allergens.objects.create(
            name=self.valid_allergen_name,
            description=self.valid_allergen_description,
        )
        self.assertTrue(Allergens.objects.get(name=self.valid_allergen_name))
        self.assertTrue(
            Allergens.objects.get(description=self.valid_allergen_description)
        )

    def test_name_allergen_uniqueness(self):
        """
        Test allergen name uniqueness.
        """
        Allergens.objects.create(
            name=self.valid_allergen_name,
            description=self.valid_allergen_description,
        )
        with self.assertRaises(IntegrityError):
            Allergens.objects.create(
                name=self.existing_allergen_name,
                description="This is a new allergen description.",
            )
            self.assertFalse(Allergens.objects.get(
                name=self.valid_allergen_name))

    def test_allergen_description_uniqueness(self):
        """
        Test allergen description uniqueness.
        """
        Allergens.objects.create(
            name=self.valid_allergen_name,
            description=self.valid_allergen_description,
        )
        with self.assertRaises(IntegrityError):
            Allergens.objects.create(
                name="New allergen name.",
                description=self.existing_allergen_description,
            )
            self.assertFalse(
                Allergens.objects.get(
                    description=self.valid_allergen_description)
            )

    def test_activities_str_method(self):
        """
        Test the __str__ method for the Allergens model.
        """
        allergen = Allergens.objects.create(
            name=self.valid_allergen_name,
            description=self.valid_allergen_description,
        )
        self.assertEqual(
            str(allergen),
            f"{
                allergen.name} - {allergen.description}",
        )
