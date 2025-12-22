from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import Seat, Theatre


class TheatreListSerializer(ModelSerializer):
    class Meta:
        model = Theatre
        fields = "__all__"
        read_only_fields = ("created_by", "available")


class SeatSerializer(ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


class NestedSeatSerializer(ModelSerializer):
    """Filters the data for normal users/admins, while the normal users can
    see either a seat occupied are not, and by which gender the admins also
    can see the user id of the user who reserved this seat
    """

    occupied_by = SerializerMethodField()

    class Meta:
        model = Seat
        fields = ["id", "occupied_by"]

    def get_occupied_by(self, obj):
        """Returns the status of requested seat (occupied, gender) for normal users while admins
        can also see the user id of the user who reserved the seat

        Args:
            obj (django.db.models.Model): The requested seat model this serializer
            is representing

        Returns:
            dict: The status of this seat
        """
        request = self.context.get("request")

        # If the seat is not occupied by anyone the result is same for admins/users
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
        """Since seats are not a theatre property, all seat objects that have the requested
        theatre set as their theatre will be queried and returned through another serializer
        so the data can be filtered for normal user/admins

        Args:
            obj (django.db.models.Model): The requested theatre model object this serializer
            is representing

        Returns:
            ModelSerializer: An instance of NestedSeatSerializer for more control over the
            data users will see
        """
        seats_qs = Seat.objects.filter(theatre=obj)
        return NestedSeatSerializer(
            seats_qs,
            many=True,
            context={"request": self.context.get("request")},
        ).data
