from rest_framework import generics

from .models import Theatre
from .permissions import AdminWriteUserReadPermission
from .serializers import TheatreSerializer


class TheatreListView(generics.ListCreateAPIView):
    queryset = Theatre.objects.all()
    serializer_class = TheatreSerializer
    permission_classes = [AdminWriteUserReadPermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TheatreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Theatre.objects.all()
    serializer_class = TheatreSerializer
    permission_classes = [AdminWriteUserReadPermission]
