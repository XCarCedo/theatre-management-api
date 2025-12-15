from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import Seat, Theatre


class TheatreListSerializer(ModelSerializer):
    class Meta:
        model = Theatre
        fields = "__all__"
        read_only_fields = ("created_by", "available")


class TheatreDetailSerializer(ModelSerializer):
    class Meta:
        model = Theatre
        fields = "__all__"
        read_only_fields = ("created_by",)


class SeatSerializer(ModelSerializer):
    occupied_by = SerializerMethodField()

    class Meta:
        model = Seat
        fields = ["id", "occupied_by"]  # only these fields

    def get_occupied_by(self, obj):
        request = self.context.get("request")

        # If the seat is not occupied by anyone the result is same for admin/users
        if not obj.occupied_by:
            return {"is_occupied": False}

        # If the seat is occupied, admins see user id and gender
        if request.user.role == "manager" or request.user.is_superuser:
            return {
                "id": obj.occupied_by.id,
                "gender": obj.occupied_by.gender,
                "is_occupied": True,
            }

        # If the seat is occupied, users see only gender
        return {"gender": obj.occupied_by.gender, "is_occupied": True}


class TheatreDetailSerializer(ModelSerializer):
    seats = SerializerMethodField()

    class Meta:
        model = Theatre
        fields = [
            "id",
            "name",
            "seats_count",
            "price",
            "seats",
        ]

    def get_seats(self, obj):
        seats_qs = Seat.objects.filter(theatre=obj)
        return SeatSerializer(
            seats_qs, many=True, context={"request": self.context.get("request")}
        ).data
