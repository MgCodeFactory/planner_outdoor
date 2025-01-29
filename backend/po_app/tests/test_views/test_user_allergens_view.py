from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ...models import Users, Allergens, UserAllergens
import os


class UserAllergensViewsetTest(APITestCase):
    """
    Test class for User Allergens viewset.
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
        self.allergen_4 = Allergens.objects.create(
            name="testallergen 4",
            description="test allergen description 4",
        )
        # instance for UserAllergens
        self.user_allergen_1 = UserAllergens.objects.create(
            user=self.auth_user, allergen=self.allergen_1
        )
        self.user_allergen_2 = UserAllergens.objects.create(
            user=self.auth_user, allergen=self.allergen_2
        )
        self.user_allergen_3 = UserAllergens.objects.create(
            user=self.staff_user, allergen=self.allergen_3
        )

    def test_user_allergens_list_unauthenticated(self):
        """
        Test that unauthenticated users can't access user allergens list.
        """
        url = reverse("user-allergens-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_allergens_list_authenticated_owner(self):
        """
        Test that authenticated users can only access his own allergen list.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-allergens-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertNotEqual(len(response.data), 3)

    def test_user_allergens_list_staff(self):
        """
        Test that staff users can access user allergens list.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("user-allergens-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_user_allergen_unauthenticated(self):
        """
        Test that unauthenticated users can't create a new user allergen.
        """
        url = reverse("user-allergens-list")
        data = {"user": self.unauth_user.id, "allergen": self.allergen_1.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(UserAllergens.objects.count(), 3)

    def test_create_user_allergen_authenticated(self):
        """
        Test that authenticated users can create a new user allergen.
        """
        url = reverse("user-allergens-list")
        data = {"user": self.auth_user.id, "allergen": self.allergen_4.id}
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserAllergens.objects.filter(
            user=self.auth_user).count(), 3)

    def test_create_allergen_staff(self):
        """
        Test that staff users can create a new user allergen.
        """
        url = reverse("user-allergens-list")
        data = {"user": self.staff_user.id, "allergen": self.allergen_1.id}
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserAllergens.objects.count(), 4)

    def test_create_user_allergen_invalid_data(self):
        """
        Test it's not possible to create a user allergen with invalid data.
        """
        url = reverse("user-allergens-list")
        data = {"user": "invalid_user", "allergen": self.allergen_1.id}
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserAllergens.objects.count(), 3)

    def test_user_allergen_retreive_unauthenticated(self):
        """
        Test that unauthenticated users can't access user allergen.
        """
        url = reverse("user-allergen-detail",
                      kwargs={"pk": self.user_allergen_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_allergen_retrieve_authenticated_owner(self):
        """
        Test that authenticated user can access only is own allergen.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-allergen-detail",
                      kwargs={"pk": self.user_allergen_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse("user-allergen-detail",
                      kwargs={"pk": self.user_allergen_3.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_allergen_retreive_staff(self):
        """
        Test that staff users can access all users allergens.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("user-allergen-detail",
                      kwargs={"pk": self.user_allergen_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse("user-allergen-detail",
                      kwargs={"pk": self.user_allergen_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_allergen_update_unauthenticated(self):
        """
        Test that unauthenticated users can't update user allergen.
        """
        url = reverse("user-allergen-detail",
                      kwargs={"pk": self.user_allergen_2.id})
        response = self.client.put(
            url, {"user": self.staff_user.id, "allergen": self.allergen_2.id}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_allergen_update_authenticated_owner(self):
        """
        Test that authenticated user can update his own allergen.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-allergen-detail",
                      kwargs={"pk": self.user_allergen_1.id})
        response = self.client.put(
            url, {"user": self.auth_user.id, "allergen": self.allergen_4.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_allergen_update_authenticated_not_owner(self):
        """
        Test that authenticated user can't update another user allergen.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-allergen-detail",
                      kwargs={"pk": self.user_allergen_3.id})
        response = self.client.put(
            url, {"user": self.auth_user.id, "allergen": self.allergen_4.id}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_allergen_update_staff(self):
        """
        Test that staff users can update all users allergens.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("user-allergen-detail",
                      kwargs={"pk": self.user_allergen_1.id})
        response = self.client.put(
            url, {"user": self.auth_user.id, "allergen": self.allergen_4.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_allergen_updated = UserAllergens.objects.get(
            id=self.user_allergen_1.id)
        self.assertEqual(user_allergen_updated.allergen.name,
                         self.allergen_4.name)
        url = reverse("user-allergen-detail",
                      kwargs={"pk": self.user_allergen_2.id})
        response = self.client.put(
            url, {"user": self.staff_user.id, "allergen": self.allergen_1.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_allergen_updated = UserAllergens.objects.get(
            id=self.user_allergen_2.id)
        self.assertEqual(user_allergen_updated.user, self.staff_user)

    def test_user_allergen_destroy_unauthenticated(self):
        """
        Test that unauthenticated users can't delete a user allergen.
        """
        url = reverse("user-allergen-detail",
                      kwargs={"pk": self.user_allergen_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_allergen_destroy_authenticated_owner(self):
        """
        Test that authenticated user can only delete his own allergen.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-allergen-detail",
                      kwargs={"pk": self.user_allergen_2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_allergen_destroy_authenticated_not_owner(self):
        """
        Test that authenticated user can't delete other user allergen.
        """
        self.client.force_authenticate(user=self.auth_user)
        url = reverse("user-allergen-detail",
                      kwargs={"pk": self.user_allergen_3.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_allergen_destroy_staff(self):
        """
        Test that staff users can delete all user allergens.
        """
        self.client.force_authenticate(user=self.staff_user)
        url = reverse("user-allergen-detail",
                      kwargs={"pk": self.user_allergen_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserAllergens.objects.count(), 2)
        url = reverse("user-allergen-detail",
                      kwargs={"pk": self.user_allergen_2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserAllergens.objects.count(), 1)
