from django.urls import path

from .views import Balance, Charge

urlpatterns = [
    path("charge/", Charge.as_view(), name="charge"),
    path("balance/", Balance.as_view(), name="balance"),
]
