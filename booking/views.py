from rest_framework import generics

from .models import Seat, Theatre
from .permissions import AdminWriteUserReadPermission
from .serializers import TheatreDetailSerializer, TheatreListSerializer


class TheatreListView(generics.ListCreateAPIView):
    queryset = Theatre.objects.all()
    serializer_class = TheatreListSerializer
    permission_classes = [AdminWriteUserReadPermission]

    def perform_create(self, serializer):
        theatre = serializer.save(created_by=self.request.user)

        seats = [
            Seat(theatre=theatre, number=i + 1, price=theatre.price)
            for i in range(theatre.seats_count)
        ]
        Seat.objects.bulk_create(seats)


class TheatreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Theatre.objects.all()
    serializer_class = TheatreDetailSerializer
    permission_classes = [AdminWriteUserReadPermission]
