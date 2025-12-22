from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminWriteUserReadPermission(BasePermission):
    """Permission only allows normal users to send safe methods (GET, HEAD, OPTIONS)
    while admins are allowed to send anything (POST, DEL, etc...)"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.is_superuser or request.user.role == "manager"

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.is_superuser or request.user.role == "manager"


class AdminOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == "manager"
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == "manager"
        )
