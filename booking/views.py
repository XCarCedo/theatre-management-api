from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from .models import Seat, Theatre
from .permissions import AdminOnlyPermission, AdminWriteUserReadPermission
from .serializers import (
    SeatSerializer,
    TheatreDetailSerializer,
    TheatreListSerializer,
)


class TheatreListView(generics.ListCreateAPIView):
    queryset = Theatre.objects.filter(available=True)
    serializer_class = TheatreListSerializer
    permission_classes = [AdminWriteUserReadPermission]

    def perform_create(self, serializer):
        """Creates the theatre with created_by set as the user sending the request and
        also creates n seats and links them to the created theatre

        Args:
            serializer (rest_framework.serializers.ModelSerializer): Current serializer
            of this view
        """
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

    def perform_update(self, serializer):
        """Makes sure the seats_count of a theatre model can only be increased and new seats
        are added to the database when that happens

        Args:
            serializer (rest_framework.serializer.ModelSerializer): Current serializer
            of this class

        Raises:
            ValidationError: In case the updated seats_count value is lesser then the previous one
        """
        theatre = self.get_object()
        old_seats_count = theatre.seats_count
        new_seats_count = serializer.validated_data.get(
            "seats_count", old_seats_count
        )

        if new_seats_count < old_seats_count:
            raise ValidationError("You cannot reduce seats count.")
        elif new_seats_count > old_seats_count:
            new_seats = [
                Seat(
                    theatre=theatre,
                    number=old_seats_count + i,
                    price=theatre.price,
                )
                for i in range(new_seats_count - old_seats_count)
            ]
            Seat.objects.bulk_create(new_seats)

        serializer.save()


class SeatDetailView(generics.RetrieveUpdateAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [AdminOnlyPermission]


class SeatReserveView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Reserves a seat if its not already reserved and the user has enough balance
        Also makes the theatre unavailable if all seats are reserved by now

        Args:
            request (rest_framework.request.Request): Request object
            pk (int): Primary key of requested seat

        Returns:
            rest_framework.response.Response: Status and message of the request
        """
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

        current_theatre_seats = Seat.objects.filter(theatre=seat.theatre)
        current_theatre_seats = map(
            lambda seat: seat.occupied_by, current_theatre_seats
        )
        if all(current_theatre_seats):
            seat.theatre.available = False
            seat.theatre.save()

        return Response({"ok": True, "message": "Seat reserved"})
