from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class BookingTests(APITestCase):
    def setUp(self):
        # manager (allowed to create theatres) and a regular customer
        self.manager = User.objects.create_user(
            username="manager",
            password="pass",
            role="manager",
            balance=Decimal("0.00"),
        )

        self.customer = User.objects.create_user(
            username="customer",
            password="pass",
            role="customer",
            balance=Decimal("0.00"),
        )

        self.theatre1 = self._create_theatre_via_api(
            self.manager, "t1", 3, "5.00"
        )
        self.theatre2 = self._create_theatre_via_api(
            self.manager, "t2", 2, "5.00"
        )
        self.theatre3 = self._create_theatre_via_api(
            self.manager, "t3", 1, "5.00"
        )

    def _create_theatre_via_api(self, user, name, seats_count, price):
        self.client.force_authenticate(user=user)
        data = {"name": name, "seats_count": seats_count, "price": price}
        response = self.client.post(reverse("theatre_list"), data)

        return response

    def test_create_theatres(self):
        error_theatre = self._create_theatre_via_api(
            self.customer, "error", 5, "5.00"
        )

        self.assertEqual(error_theatre.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(self.theatre1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.theatre2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.theatre3.status_code, status.HTTP_201_CREATED)

    def test_list_theatres(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(reverse("theatre_list"))
        data = response.json()

        self.assertEqual(data[0]["id"], self.theatre1.json()["id"])
        self.assertEqual(data[1]["id"], self.theatre2.json()["id"])
        self.assertEqual(data[2]["id"], self.theatre3.json()["id"])

    def test_theatre_detail_update(self):
        self.client.force_authenticate(user=self.manager)
        response_valid = self.client.patch(
            reverse(
                "theatre_detail", kwargs={"pk": self.theatre1.json()["id"]}
            ),
            {"seats_count": 5},
        )
        response_valid_status = self.client.get(
            reverse(
                "theatre_detail", kwargs={"pk": self.theatre1.json()["id"]}
            )
        )

        self.assertEqual(response_valid.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_valid_status.json()["seats"]), 5)
