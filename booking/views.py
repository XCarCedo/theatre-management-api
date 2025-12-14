from rest_framework import generics

from .models import Theatre
from .permissions import AdminWriteUserReadPermission
from .serializers import TheatreDetailSerializer, TheatreListSerializer


class TheatreListView(generics.ListCreateAPIView):
    queryset = Theatre.objects.all()
    serializer_class = TheatreListSerializer
    permission_classes = [AdminWriteUserReadPermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TheatreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Theatre.objects.all()
    serializer_class = TheatreDetailSerializer
    permission_classes = [AdminWriteUserReadPermission]
