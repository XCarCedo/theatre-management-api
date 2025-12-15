from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Seat, Theatre
from .permissions import AdminWriteUserReadPermission
from .serializers import TheatreDetailSerializer, TheatreListSerializer


class TheatreListView(generics.ListCreateAPIView):
    queryset = Theatre.objects.filter(available=True)
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


class SeatReserveView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        seat = get_object_or_404(Seat, pk=pk)

        if seat.occupied_by is not None:
            return Response(
                {"ok": False, "message": "Seat already occupied"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not request.user.balance >= seat.price:
            return Response(
                {"ok": False, "message": "Balance is not enough"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.balance = F("balance") - seat.price
        seat.occupied_by = request.user
        seat.save()

        return Response({"ok": True, "message": "Seat reserved"})
