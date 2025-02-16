from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import json
import re


@deconstructible
class CustomUsernameValidator:
    """
    Custom username validator for Users.
    """

    def __call__(self, username):
        """
        Validate username in serializer.
        """
        if not isinstance(username, str):
            raise ValidationError("Username must be a valid string.")
        if re.match(r"^[\s]+$", username):
            raise ValidationError("Username cantt be blank.")
        if username.isdigit():
            raise ValidationError("Username must not contains only digit.")
        if not re.match(r"^[a-zA-Z0-9\s_-]+$", username):
            raise ValidationError(
                "Username must not contain special characters (except: _ -)."
            )

    def get_help_text(self):
        """
        Returns a help text for the username validator.
        """
        return "Valid username: a string, length less than 50, no special characters (except: _ -)."


@deconstructible
class CustomPasswordValidator:
    """
    Custom password validator for Users.
    """

    def __call__(self, password):
        """
        Validate the password in serializer.
        """
        if password is None:
            raise ValidationError("Password can't be null.")
        if len(password) < 8:
            raise ValidationError(
                "Password must be at least 8 characters long.")
        if not re.findall("[A-Z]", password):
            raise ValidationError(
                "Password must contain at least one uppercase character."
            )
        if not re.findall("[a-z]", password):
            raise ValidationError(
                "Password must contain at least one lowercase character."
            )
        if not re.findall("[0-9]", password):
            raise ValidationError("Password must contain at least one number.")
        if not re.findall("[^A-Za-z0-9]", password):
            raise ValidationError(
                "Password must contain at least one special character."
            )

        for char in password:
            if password.count(char) > 1:
                raise ValidationError(
                    "In password, all characters must be different.")

    def get_help_text(self):
        """
        Returns a help text for the password validator.
        """
        return "Valid password: At least 8 characters, one uppercase, one lowercase, one number, one special character, and all different."


@deconstructible
class CustomLocationValidator:
    """
    Custom location validator for Users and PlannedActivities.
    """

    def __call__(self, location):
        """
        Validate location in serializer.
        """
        # init regex
        required_keys = ["name", "lat", "lon", "country"]
        regex_name = r"^[a-zA-Z\s]+$"
        regex_country = r"^[A-Z]+$"
        # tests location validation
        try:
            json.dumps(location)
        except TypeError:
            raise ValidationError("Location must be a valid JSON.")
        if location is None:
            raise ValidationError("Location can't be null.")
        if not all(key in location for key in required_keys):
            raise ValidationError(
                "Location must contain all required keys: name, lat, lon, country code."
            )
        if not all(location[key] for key in required_keys):
            raise ValidationError(
                "Location must contain all required values: name, lat, lon, country code."
            )
        if not isinstance(location["name"], str):
            raise ValidationError("Location name must a valid string.")
        if location["name"].isspace():
            raise ValidationError("Location name must not be empty.")
        if not re.match(regex_name, location["name"]):
            raise ValidationError("Location name must contain only letters.")
        if not isinstance(location["lat"], (int, float)):
            raise ValidationError(
                "Location latitude must be a valid float number.")
        if not -90 <= location["lat"] <= 90:
            raise ValidationError(
                "Location latitude must be between -90 and 90.")
        if not isinstance(location["lon"], (int, float)):
            raise ValidationError(
                "Location longitude must be a valid float number.")
        if not -180 <= location["lon"] <= 180:
            raise ValidationError(
                "Location longitude must be between -180 and 180.")
        if not isinstance(location["country"], str):
            raise ValidationError("Location country must be a valid string.")
        if location["country"].isspace():
            raise ValidationError("Location country must not be empty.")
        if not location["country"].isupper():
            raise ValidationError(
                "Location country code must be uppercase letters.")
        if not re.match(regex_country, location["country"]):
            raise ValidationError(
                "Location country code must contain only A-Z letters."
            )

    def get_help_text(self):
        """
        Returns a help text for the location validator.
        """
        return "Valid location: Must be a valid JSON dictionary, with keys: name, lat, lon, country and valid values inside."


@deconstructible
class CustomNameValidator:
    """
    Custom name validator for Activities.
    """

    def __call__(self, name):
        """
        Validate name in serializer.
        """
        if not isinstance(name, str):
            raise ValidationError("Name must be a valid string.")
        if name.isdigit():
            raise ValidationError("Name must not contains only digit.")
        if name.isspace():
            raise ValidationError("Name must not be empty.")
        if not re.match(r"^[a-zA-Z0-9\s.-]+$", name):
            raise ValidationError(
                "Name must not contain special characters (except: . -)."
            )

    def get_help_text(self):
        """
        Returns a help text for the name validator.
        """
        return "Valid name: a string, length less than 50, no special characters (except: . -)."


@deconstructible
class CustomDescriptionValidator:
    """
    Custom description validator for Activities.
    """

    def __call__(self, description):
        """
        Validate description in serializer.
        """
        if not isinstance(description, str):
            raise ValidationError("Descrition must be a valid string.")
        if description.isdigit():
            raise ValidationError("Descrition must not contain only digit.")
        if description.isspace():
            raise ValidationError("Descrition must not be empty.")
        if not re.match(r"^[a-zA-Z0-9\s.,!-]+$", description):
            raise ValidationError(
                "Description must not contain special characters (except: . , ! -)."
            )

    def get_help_text(self):
        """
        Returns a help text for the description validator.
        """
        return "Valid description: a string, length less than 200, no special characters (except: . , ! -)."
