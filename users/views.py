from django.db.models import F
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import ChargeSerializer

UNEXCEPTED_ERROR_RESPONSE = Response(
    {"success": False, "message": "An unexpected error occurred."},
    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
)


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
            return UNEXCEPTED_ERROR_RESPONSE

        return Response(
            {"success": True, "message": "Account charged successfully"},
            status=status.HTTP_200_OK,
        )


class Balance(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            balance = request.user.balance
        except:
            return UNEXCEPTED_ERROR_RESPONSE

        return Response({"success": True, "balance": balance})
