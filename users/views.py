from django.db.models import F
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import ChargeSerializer


class Charge(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChargeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]

        try:
            request.user.balance = F("balance") + amount
            request.user.save()
            request.user.refresh_from_db()
        except Exception:
            return Response(
                {"success": False, "message": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"success": True, "message": "Account charged successfully"},
            status=status.HTTP_200_OK,
        )
