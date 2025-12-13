from rest_framework.serializers import ModelSerializer

from .models import Theatre


class TheatreSerializer(ModelSerializer):
    class Meta:
        model = Theatre
        fields = "__all__"
        read_only_fields = ("created_by", "available")
