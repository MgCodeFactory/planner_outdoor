from .test_models_common import BaseLocationTestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ...models import Users
from ...validators import (
    CustomUsernameValidator,
    CustomPasswordValidator,
)
import os


class UsersTestCase(BaseLocationTestCase):
    """
    Tests for Users model.
    """

    def setUp(self):
        """
        Set up the test data for Users model.
        """
        super().setUp()
        # data for username
        self.invalid_useranme_len = "x" * 51
        self.invalid_username_type = 123
        self.invalid_username_null = None
        self.invalid_username_blank = "     "
        self.existing_username = self.valid_username
        self.invalid_username_bad_special = "testuser#"
        # data for password
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
        self.invalid_password_null = None
        self.invalid_password_blank = " "
        # data for email
        self.invalid_email = "invalid_email"
        self.existing_email = self.valid_email
        self.invalid_email_type = 123
        self.invalid_email_null = None
        self.invalid_email_blank = " "

    def test_valid_password(self):
        """
        Test valid password.
        """
        validator = CustomPasswordValidator()
        validator(self.valid_password)

    def test_invalid_password_len(self):
        """
        Test invalid password using CustomPasswordValidator.test_location_null
        """
        with self.assertRaises(ValidationError):
            CustomPasswordValidator()(self.invalid_password_len)

    def test_invalid_password_type(self):
        """
        Test invalid password type.
        """
        with self.assertRaises(ValidationError):
            CustomPasswordValidator()(self.invalid_password_type)

    def test_invalid_password_no_upper(self):
        """
        Test invalid password no uppercase character.
        """
        with self.assertRaises(ValidationError):
            CustomPasswordValidator()(self.invalid_password_no_upper)

    def test_invalid_password_no_lower(self):
        """
        Test invalid password no lowercase character.
        """
        with self.assertRaises(ValidationError):
            CustomPasswordValidator()(self.invalid_password_no_lower)

    def test_invalid_password_no_digit(self):
        """
        Test invalid password no digit character.
        """
        with self.assertRaises(ValidationError):
            CustomPasswordValidator()(self.invalid_password_no_digit)

    def test_invalid_password_no_special(self):
        """
        Test invalid password no special character.
        """
        with self.assertRaises(ValidationError):
            CustomPasswordValidator()(self.invalid_password_no_special)

    def invalid_password_no_diff(self):
        """
        Test invalid password 2 or more character repeated.
        """
        with self.assertRaises(ValidationError):
            CustomPasswordValidator()(self.invalid_password_no_diff)

    def test_invalid_password_null(self):
        """
        Test invalid password null value.
        """
        with self.assertRaises(ValidationError):
            CustomPasswordValidator()(self.invalid_password_null)

    def test_invalid_password_blank(self):
        """
        Test invalid password blank value.
        """
        with self.assertRaises(ValidationError):
            CustomPasswordValidator()(self.invalid_password_blank)

    def test_create_valid_user(self):
        """
        Test creating a valid user.
        """
        Users.objects.create_user(
            username=self.valid_username,
            email=self.valid_email,
            password=self.valid_password,
            location=self.valid_location,
        )
        self.assertTrue(Users.objects.get(username=self.valid_username))

    def test_create_user_save(self):
        """
        Test creating user save method.
        """
        user = Users.objects.create_user(
            username="testuser_2",
            email="testuser_2@example.com",
            password=self.valid_password,
            location=self.valid_location,
        )
        user.save()
        self.assertTrue(Users.objects.get(username="testuser_2"))
        self.assertNotEqual(user.password, self.valid_password)

    def test_invalid_username_type(self):
        """
        Test invalid username type.
        """
        with self.assertRaises(ValidationError):
            CustomUsernameValidator()(self.invalid_username_type)

    def test_invalid_username_bad_special(self):
        """
        Test invalid username with bad special character.
        """
        with self.assertRaises(ValidationError):
            CustomUsernameValidator()(self.invalid_username_bad_special)

    def test_invalid_username_len(self):
        """
        Test invalid username length.
        """
        user = Users(
            username=self.invalid_useranme_len,
            email=self.valid_email,
            password=self.valid_password,
            location=self.valid_location,
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_invalid_username_null(self):
        """
        Test invalid username null value.
        """
        user = Users(
            username=self.invalid_username_null,
            email=self.valid_email,
            password=self.valid_password,
            location=self.valid_location,
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_invalid_username_blank(self):
        """
        Test invalid username blank value.
        """
        user = Users(
            username=self.invalid_username_blank,
            email=self.valid_email,
            password=self.valid_password,
            location=self.valid_location,
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_username_uniqueness(self):
        """
        Test username uniqueness.
        """
        Users.objects.create_user(
            username=self.valid_username,
            email=self.valid_email,
            password=self.valid_password,
            location=self.valid_location,
        )
        with self.assertRaises(IntegrityError):
            Users.objects.create_user(
                username=self.valid_username,
                email=self.valid_email,
                password=self.valid_password,
                location=self.valid_location,
            )
            self.assertFalse(Users.objects.get(username=self.valid_username))

    def test_email_uniqueness(self):
        """
        Test email uniqueness.
        """
        Users.objects.create_user(
            username=self.valid_username,
            email=self.valid_email,
            password=self.valid_password,
            location=self.valid_location,
        )
        with self.assertRaises(IntegrityError):
            Users.objects.create_user(
                username=self.valid_username,
                email=self.valid_email,
                password=self.valid_password,
                location=self.valid_location,
            )
            self.assertFalse(Users.objects.get(username=self.valid_username))

    def test_invalid_email(self):
        """
        Test invalid email.
        """
        user = Users(
            username=self.valid_username,
            email=self.invalid_email,
            password=self.valid_password,
            location=self.valid_location,
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_invalid_email_type(self):
        """
        Test invalid email type.
        """
        user = Users(
            username=self.valid_username,
            email=self.invalid_email_type,
            password=self.valid_password,
            location=self.valid_location,
        )
        with self.assertRaises(AttributeError):
            user.full_clean()

    def test_invalid_email_null(self):
        """
        Test invalid email null value.
        """
        user = Users(
            username=self.valid_username,
            email=self.invalid_email_null,
            password=self.valid_password,
            location=self.valid_location,
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_invalid_email_blank(self):
        """
        Test invalid email blank value.
        """
        user = Users(
            username=self.valid_username,
            email=self.invalid_email_blank,
            password=self.valid_password,
            location=self.valid_location,
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_existing_usermame(self):
        """
        Test creating a user with an existing username.
        """
        user = Users.objects.create_user(
            username=self.valid_username,
            email=self.valid_email,
            password=self.valid_password,
            location=self.valid_location,
        )

        with self.assertRaises(Exception):
            new_user = Users.objects.create_user(
                username=user.username,
                email="new_test@example.com",
                password=self.valid_password,
                location=self.valid_location,
            )
            self.assertEqual(new_user.username, user.username)

    def test_existing_email(self):
        """
        Test creating a user with an existing email.
        """
        user = Users.objects.create_user(
            username=self.valid_username,
            email=self.valid_email,
            password=self.valid_password,
            location=self.valid_location,
        )
        with self.assertRaises(Exception):
            new_user = Users.objects.create_user(
                username="new testuser",
                email=user.email,
                password=self.valid_password,
                location=self.valid_location,
            )
            self.assertEqual(new_user.email, user.email)

    def test_location_null(self):
        """
        Test user location null value.
        """
        user = Users(
            username=self.valid_username,
            email=self.valid_email,
            password=self.valid_password,
            location=self.invalid_location_null,
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_location_blank(self):
        """
        Test user location blank value.
        """
        user = Users(
            username=self.valid_username,
            email=self.valid_email,
            password=self.valid_password,
            location=self.invalid_location_blank,
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_users_str_method(self):
        """
        Test the __str__ method of the Users model.
        """
        user = Users.objects.create_user(
            username=self.valid_username,
            email=self.valid_email,
            password=self.valid_password,
            location=self.valid_location,
        )
        self.assertEqual(str(user), f"{user.username} - {user.email}")
