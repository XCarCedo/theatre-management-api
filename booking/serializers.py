from rest_framework.serializers import ModelSerializer

from .models import Theatre


class TheatreListSerializer(ModelSerializer):
    class Meta:
        model = Theatre
        fields = "__all__"
        read_only_fields = ("created_by", "available")


class TheatreDetailSerializer(ModelSerializer):
    class Meta:
        model = Theatre
        fields = "__all__"
        read_only_fields = "created_by"
