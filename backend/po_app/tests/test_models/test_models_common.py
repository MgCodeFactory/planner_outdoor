from django.core.exceptions import ValidationError
from django.test import TestCase
import os
from ...validators import (
    CustomLocationValidator,
    CustomNameValidator,
    CustomDescriptionValidator,
)
from ...models import (
    Activities,
    Allergens,
)


class BaseLocationTestCase(TestCase):
    """
    Base class for testing location validators.
    """

    def setUp(self):
        """
        Setup data for location tests.
        """
        # data for valid user needed for location tests
        self.valid_username = "testuser"
        self.valid_email = "test@example.com"
        self.valid_password = os.environ.get("VALID_PASSWORD")
        # data for location
        self.valid_location = {
            "name": "London",
            "lat": 51.5073219,
            "lon": -0.1276474,
            "country": "GB",
        }
        # invalid location general
        self.invalid_location_null = None
        self.invalid_location_blank = "  "
        self.invalid_location_not_json = "invalid json type"
        self.invalid_location_missing_keys = {
            "A": "London",
            "B": 51.5073219,
            "C": -0.1276474,
            "D": "GB",
            "E": "England",
        }
        self.invalid_location_missing_values = {
            "name": None,
            "lat": None,
            "lon": None,
            "country": None,
        }
        # invalid location "name"
        self.invalid_location_missing_key_name = {
            "lat": 51.5073219,
            "lon": -0.1276474,
            "country": "GB",
        }
        self.invalid_location_missing_value_name = {
            "name": None,
            "lat": 51.5073219,
            "lon": -0.1276474,
            "country": "GB",
        }
        self.invalid_location_name_type = {
            "name": 123,
            "lat": 51.5073219,
            "lon": -0.1276474,
            "country": "GB",
        }
        self.invalid_location_name_null = {
            "name": None,
            "lat": 51.5073219,
            "lon": -0.1276474,
            "country": "GB",
        }
        self.invalid_location_name_blank = {
            "name": " ",
            "lat": 51.5073219,
            "lon": -0.1276474,
            "country": "GB",
        }
        # invalid location "lat"
        self.invalid_location_missing_key_lat = {
            "name": "London",
            "lon": -0.1276474,
            "country": "GB",
        }
        self.invalid_location_missing_value_lat = {
            "name": "London",
            "lat": None,
            "lon": -0.1276474,
            "country": "GB",
        }
        self.invalid_location_lat_type = {
            "name": "London",
            "lat": "latitude",
            "lon": -0.1276474,
            "country": "GB",
        }
        self.invalid_location_lat_null = {
            "name": "London",
            "lat": None,
            "lon": -0.1276474,
            "country": "GB",
        }
        self.invalid_location_lat_blank = {
            "name": "London",
            "lat": "",
            "lon": -0.1276474,
            "country": "GB", ,
        }
        self.invalid_location_lat_out_of_range = {
            "name": "London",
            "lat": 100,
            "lon": -0.1276474,
            "country": "GB",
        }
        # invalid location "lon"
        self.invalid_location_missing_key_lon = {
            "name": "London",
            "lat": 51.5073219,
            "country": "GB",
        }
        self.invalid_location_missing_value_lon = {
            "name": "London",
            "lat": 51.5073219,
            "lon": None,
            "country": "GB",
        }
        self.invalid_location_lon_type = {
            "name": "London",
            "lat": 51.5073219,
            "lon": "longitude",
            "country": "GB", ,
        }
        self.invalid_location_lon_null = {
            "name": "London",
            "lat": 51.5073219,
            "lon": None,
            "country": "GB",
        }
        self.invalid_location_lon_blank = {
            "name": "London",
            "lat": 51.5073219,
            "lon": "",
            "country": "GB",
        }
        self.invalid_location_lon_out_of_range = {
            "name": "London",
            "lat": 51.5073219,
            "lon": 200,
            "country": "GB",
        }
        # invalid location "country"
        self.invalid_location_missing_key_country = {
            "name": "London",
            "lat": 51.5073219,
            "lon": -0.1276474,
        }
        self.invalid_location_missing_value_country = {
            "name": "London",
            "lat": 51.5073219,
            "lon": -0.1276474,
            "country": None,
        }
        self.invalid_location_country_type = {
            "name": "London",
            "lat": 51.5073219,
            "lon": -0.1276474,
            "country": 123,
        }
        self.invalid_location_country_null = {
            "name": "London",
            "lat": 51.5073219,
            "lon": -0.1276474,
            "country": None,
        }
        self.invalid_location_country_blank = {
            "name": "London",
            "lat": 51.5073219,
            "lon": -0.1276474,
            "country": " ",
        }

    def test_invalid_location_not_json(self):
        """
        Test invalid location not valid JSON.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_not_json)

    def test_invalid_location_missing_keys(self):
        """
        Test invalid location missing keys.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_missing_keys)

    def test_invalid_location_missing_values(self):
        """
        Test invalid location missing values.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_missing_values)

    def test_invalid_location_missing_key_name(self):
        """
        Test invalid location missing key "name".
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_missing_key_name)

    def test_invalid_location_missing_value_name(self):
        """
        Test invalid location missing value for key "name".
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_missing_value_name)

    def test_invalid_location_name_type(self):
        """
        Test invalid location name type.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_name_type)

    def test_invalid_location_name_null(self):
        """
        Test invalid location name null value.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_name_null)

    def test_invalid_location_name_blank(self):
        """
        Test invalid location name blank value.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_name_blank)

    def test_invalid_location_missing_key_lat(self):
        """
        Test invalid location missing key "lat".
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_missing_key_lat)

    def test_invalid_location_missing_value_lat(self):
        """
        Test invalid location missing value for key "lat".
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_missing_value_lat)

    def test_invalid_location_lat_type(self):
        """
        Test invalid location lat type.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_lat_type)

    def test_invalid_location_lat_null(self):
        """
        Test invalid location lat null value.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_lat_null)

    def test_invalid_location_lat_blank(self):
        """
        Test invalid location lat blank value.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_lat_blank)

    def test_invalid_location_lat_out_of_range(self):
        """
        Test invalid location lat out of range.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_lat_out_of_range)

    def test_invalid_location_missing_key_lon(self):
        """
        Test invalid location missing key "lon".
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_missing_key_lon)

    def test_invalid_location_missing_value_lon(self):
        """
        Test invalid location missing value for key "lon".
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_missing_value_lon)

    def test_invalid_location_lon_type(self):
        """
        Test invalid location lon type.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_lon_type)

    def test_invalid_location_lon_null(self):
        """
        Test invalid location lon null value.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_lon_null)

    def test_invalid_location_lon_blank(self):
        """
        Test invalid location lon blank value.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_lon_blank)

    def test_invalid_location_lon_out_of_range(self):
        """
        Test invalid location lon out of range.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_lon_out_of_range)

    def test_invalid_location_missing_key_country(self):
        """
        Test invalid location missing key "country".
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_missing_key_country)

    def test_invalid_location_missing_value_country(self):
        """
        Test invalid location missing value for key "country".
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_missing_value_country)

    def test_invalid_location_country_type(self):
        """
        Test invalid location country type.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_country_type)

    def test_invalid_location_country_null(self):
        """
        Test invalid location country null value.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_country_null)

    def test_invalid_location_country_blank(self):
        """
        Test invalid location country blank value.
        """
        with self.assertRaises(ValidationError):
            CustomLocationValidator()(self.invalid_location_country_blank)


class BaseNameDescriptionTestCase(TestCase):
    """
    Base class for testing name and description fields.
    """

    def setUp(self):
        """
        Set up data.
        """
        # data for name
        self.valid_activity_name = "Test activity"
        self.valid_allergen_name = "Test allergen"
        self.invalid_name_len = "x" * 51
        self.existing_activity_name = self.valid_activity_name
        self.existing_allergen_name = self.valid_allergen_name
        self.invalid_name_type = 123
        self.invalid_name_null = None
        self.invalid_name_blank = "   "
        self.invalid_name_bad_special = "Test invalid_special character #"
        # data for description
        self.valid_activity_description = "This is a test activity description."
        self.valid_allergen_description = "This is a test allergen description."
        self.invalid_description_len = "x" * 201
        self.existing_activity_description = self.valid_activity_description
        self.existing_allergen_description = self.valid_allergen_description
        self.invalid_description_type = 123
        self.invalid_description_null = None
        self.invalid_description_blank = " "
        self.invalid_description_bad_special = "Test invalid_special character #"

    def test_invalid_name_type(self):
        """
        Test invalid name type.
        """
        with self.assertRaises(Exception):
            CustomNameValidator()(self.invalid_name_type)

    def test_invalid_name_bad_special(self):
        """
        Test invalid name with bad special characters.
        """
        with self.assertRaises(Exception):
            CustomNameValidator()(self.invalid_name_bad_special)

    def test_invalid_name_blank(self):
        """
        Test invalid name blank value.
        """
        with self.assertRaises(ValidationError):
            CustomNameValidator()(self.invalid_name_blank)

    def test_invalid_name_len(self):
        """
        Test invalid name length.
        """
        activity = Activities(
            name=self.invalid_name_len,
            description=self.valid_activity_description,
        )
        with self.assertRaises(ValidationError):
            activity.full_clean()

        allergen = Allergens(
            name=self.invalid_name_len,
            description=self.valid_allergen_description,
        )
        with self.assertRaises(ValidationError):
            allergen.full_clean()

    def test_invalid_name_null(self):
        """
        Test invalid name null value.
        """
        activity = Activities(
            name=self.invalid_name_null,
            description=self.valid_activity_description,
        )
        with self.assertRaises(ValidationError):
            activity.full_clean()

        allergen = Allergens(
            name=self.invalid_name_null,
            description=self.valid_allergen_description,
        )
        with self.assertRaises(ValidationError):
            allergen.full_clean()

    def test_invalid_description_type(self):
        """
        Test invalid description type.
        """
        with self.assertRaises(Exception):
            CustomDescriptionValidator()(self.invalid_description_type)

    def test_invalid_description_bad_special(self):
        """
        Test invalid description with bad special characters.
        """
        with self.assertRaises(Exception):
            CustomDescriptionValidator()(self.invalid_description_bad_special)

    def test_invalid_description_blank(self):
        """
        Test invalid description blank value.
        """
        with self.assertRaises(ValidationError):
            CustomDescriptionValidator()(self.invalid_description_blank)

    def test_invalid_description_len(self):
        """
        Test invalid description length.
        """
        activity = Activities(
            name=self.valid_activity_name,
            description=self.invalid_description_len,
        )
        with self.assertRaises(ValidationError):
            activity.full_clean()

        allergen = Allergens(
            name=self.valid_allergen_name,
            description=self.invalid_description_len,
        )
        with self.assertRaises(ValidationError):
            allergen.full_clean()

    def test_invalid_description_null(self):
        """
        Test invalid description null value.
        """
        activity = Activities(
            name=self.valid_activity_name,
            description=self.invalid_description_null,
        )
        with self.assertRaises(ValidationError):
            activity.full_clean()

        allergen = Allergens(
            name=self.valid_allergen_name,
            description=self.invalid_description_null,
        )
        with self.assertRaises(ValidationError):
            allergen.full_clean()
