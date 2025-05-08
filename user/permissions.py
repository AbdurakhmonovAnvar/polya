from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.lower() == 'admin'


class IsModeratorRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.lower() == 'moderator'


class IsAdminAndModeratorRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.lower() == 'moderator' or request.user.role.lower() == 'admin'