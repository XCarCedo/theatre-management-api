from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminWriteUserReadPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if type(request.user) is AnonymousUser:
            return False

        return request.user.is_superuser or request.user.role == "manager"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if type(request.user) is AnonymousUser:
            return False

        return request.user.is_superuser or request.user.role == "manager"
