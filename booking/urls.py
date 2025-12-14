from django.urls import path

from . import views

urlpatterns = [
    path("", views.TheatreListView.as_view(), name="theatre_list"),
    path("<int:pk>/", views.TheatreDetailView.as_view(), name="theatre_detail"),
    path("reserve/<int:pk>/", views.SeatReserveView.as_view(), name="reserve_seat"),
]
