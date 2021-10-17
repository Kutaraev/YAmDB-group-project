from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_administrator


class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            not request.user.is_superuser
            and request.method not in permissions.SAFE_METHODS
        ):
            return False
        return not (
            request.user.is_anonymous
            and request.method not in permissions.SAFE_METHODS
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
            or request.user.is_moderator
        ):
            return True
        return obj.author == request.user
