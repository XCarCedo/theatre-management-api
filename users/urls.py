from django.urls import path

from .views import Balance, Charge

urlpatterns = [
    path("charge/", Charge.as_view()),
    path("balance/", Balance.as_view()),
]
