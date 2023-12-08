from rest_framework.permissions import BasePermission


class IsUserAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsUserORAdminAuthenticated(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.isAdmin
