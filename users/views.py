from decimal import Decimal

from django.db.models import F
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class Charge(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request: Request, *args, **kwargs):
        amount = request.data.get("amount", None)

        if amount == None:
            return Response(
                {"success": False, "message": "Amount is null/invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            amount = Decimal(amount)
        except:
            return Response(
                {
                    "success": False,
                    "message": "Cannot convert the given amount to a decimal value.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            request.user.balance = F("balance") + amount
            request.user.save()
        except:
            return Response(
                {"success": False, "message": "An unexcepted error occured."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"success": True, "message": "Account charged successfully"},
            status=status.HTTP_200_OK,
        )
