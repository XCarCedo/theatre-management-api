from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from .models import User


class ApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.normal_user = get_user_model().objects.create_user(
            username="normal_user", password="normal_user", role="customer"
        )
        cls.manager_user = get_user_model().objects.create_user(
            username="manager_user", password="manager_user", role="manager", balance=5
        )

        client = APIClient()

        cls.normal_user_token = client.post(
            "/api/v1/auth/login",
            data={"username": "normal_user", "password": "normal_user"},
        ).json()["key"]
        cls.manager_user_token = client.post(
            "/api/v1/auth/login",
            data={"username": "manager_user", "password": "manager_user"},
        ).json()["key"]

    def test_charging_and_balance(self):
        ### Normal user
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.normal_user_token}")
        # Reassure normal_user balance is zero
        self.assertEqual(self.client.get(reverse("balance")).json()["balance"], 0)

        self.assertEqual(
            self.client.post(reverse("charge"), data={"amount": 10}).json()["success"],
            True,
        )
        self.normal_user.refresh_from_db()
        self.assertEqual(self.normal_user.balance, 10)
        ### Manager user

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.manager_user_token}")
        # Reassure normal_user balance is zero
        self.assertEqual(self.client.get(reverse("balance")).json()["balance"], 5)

        self.assertEqual(
            self.client.post(reverse("charge"), data={"amount": 10}).json()["success"],
            True,
        )
        self.manager_user.refresh_from_db()
        self.assertEqual(self.manager_user.balance, 15)
