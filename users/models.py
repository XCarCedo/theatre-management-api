from decimal import Decimal
from random import randint

from django.contrib.auth.models import AbstractUser
from django.db import models


def generate_random_name():
    return f"user_{randint(100_000_000, 999_999_999)}"


class User(AbstractUser):
    class Role(models.TextChoices):
        customer = ("customer", "Customer")
        manager = ("manager", "Manager")

    full_name = models.CharField(default=generate_random_name, max_length=50)
    role = models.CharField(max_length=8, choices=Role.choices, default=Role.customer)
    balance = models.DecimalField(
        decimal_places=2, default=Decimal("0.00"), max_digits=10
    )

    class Gender(models.TextChoices):
        male = ("male", "Male")
        female = ("female", "Female")

    gender = models.CharField(max_length=6, default=Gender.male, choices=Gender.choices)
