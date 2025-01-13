from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ...models import Users, Allergens
import os


class AllergensViewsetTest(APITestCase):
    """
    Test class for Allergens viewset.
    """

    def setUp(self):
        # instance unauthenticated user
        self.unauth_user = Users.objects.create_user(
            username="test_unauth_user",
            email="test_unauth_user@example.com",
            password=os.environ.get("VALID_PASSWORD"),
            location={
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
                "state": "England",
            },
        )
        # instance authenticated user
        self.auth_user = Users.objects.create_user(
            username="test_auth_user",
            email="test_auth_user@example.com",
            password=os.environ.get("VALID_PASSWORD"),
            location={
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
                "state": "England",
            },
        )
        # instance staff user
        self.staff_user = Users.objects.create_user(
            username="test_staff_user",
            email="test_staff_user@example.com",
            password=os.environ.get("VALID_PASSWORD"),
            location={
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
                "state": "England",
            },
            is_staff=True,
        )
        # instance for Allergens
        self.allergen_1 = Allergens.objects.create(
            name="testallergen 1",
            description="test allergen description 1",
        )
        self.allergen_2 = Allergens.objects.create(
            name="testallergen 2",
            description="test allergen description 2",
        )
        self.allergen_3 = Allergens.objects.create(
            name="testallergen 3",
            description="test allergen description 3",
        )

    def test_allergens_list_unauthenticated(self):
        """
        Test that unauthenticated users can't access allergens list.
        """
        url = reverse("allergens-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_allergens_list_authenticated(self):
        """
        Test that authenticated users can access allergens list.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("allergens-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_allergens_list_staff(self):
        """
        Test that staff users can access allergens list.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("allergens-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_allergen_unauthenticated(self):
        """
        Test that unauthenticated users can't create a new allergen.
        """
        url = reverse("allergens-list")
        data = {
            "name": "testallergen 4",
            "description": "test allergen description 4",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Allergens.objects.count(), 3)

    def test_create_allergen_authenticated(self):
        """
        Test that authenticated users can't create a new allergen.
        """
        url = reverse("allergens-list")
        data = {"name": "testallergen 4",
                "description": "test allergen description 4"}
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Allergens.objects.count(), 3)

    def test_create_allergen_staff(self):
        """
        Test that staff users can create a new allergen.
        """
        url = reverse("allergens-list")
        data = {
            "name": "testallergen 4",
            "description": "test allergen description 4",
        }
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Allergens.objects.count(), 4)
        self.assertEqual(response.data["name"], "testallergen 4")

    def test_create_allergen_invalid_data(self):
        """
        Test it's not possible to create an allergen with invalid data.
        """
        url = reverse("allergens-list")
        data = {
            "name": 123,
            "description": "test allergen description 5",
        }
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Allergens.objects.count(), 3)

    def test_allergen_retreive_unauthenticated(self):
        """
        Test that unauthenticated users can't access allergen details.
        """
        url = reverse("allergen-detail", kwargs={"pk": self.allergen_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_allergen_retrieve_authenticated(self):
        """
        Test that authenticated users can't access allergen details.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("allergen-detail", kwargs={"pk": self.allergen_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allergen_retreive_staff(self):
        """
        Test that staff users can access all allergens details.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("allergen-detail", kwargs={"pk": self.allergen_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse("allergen-detail", kwargs={"pk": self.allergen_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_allergen_partial_update_unauthenticated(self):
        """
        Test that unauthenticated users can't update allergen details.
        """
        url = reverse("allergen-detail", kwargs={"pk": self.allergen_2.id})
        response = self.client.patch(url, {"name": "new allergen name"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_partial_update_authenticated(self):
        """
        Test that authenticated users can't update allergen details.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("allergen-detail", kwargs={"pk": self.allergen_3.id})
        response = self.client.patch(
            url, {"description": "new allergen description"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allergen_partial_update_staff(self):
        """
        Test that staff users can update all allergen details.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("allergen-detail", kwargs={"pk": self.allergen_1.id})
        response = self.client.patch(url, {"name": "updated allergen name 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "updated allergen name 1")
        url = reverse("allergen-detail", kwargs={"pk": self.allergen_3.id})
        response = self.client.patch(
            url, {"description": "updated allergen description 3"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"],
                         "updated allergen description 3")

    def test_users_destroy_unauthenticated(self):
        """
        Test that unauthenticated users can't delete allergen.
        """
        url = reverse("allergen-detail", kwargs={"pk": self.allergen_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_allergen_destroy_authenticated(self):
        """
        Test that authenticated users can't delete allergen.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("allergen-detail", kwargs={"pk": self.allergen_2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allergen_destroy_staff(self):
        """
        Test that staff users can delete all allergens.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("allergen-detail", kwargs={"pk": self.allergen_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Allergens.objects.count(), 2)
        url = reverse("allergen-detail", kwargs={"pk": self.allergen_2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Allergens.objects.count(), 1)
