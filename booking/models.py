from django.db import models

from users.models import User


class Theatre(models.Model):
    name = models.CharField(max_length=300)
    seats_count = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name


class Seat(models.Model):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    occupied_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    number = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
