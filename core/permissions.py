from rest_framework import permissions
from core.models import Role


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or \
            view.action in ['update', 'partial_update', 'change_password'] or \
            request.user.role == Role.MANAGER

    def has_object_permission(self, request, view, obj):
        return view.action in ['retrieve', 'update',
                               'partial_update', 'change_password'] or \
            request.user.role == Role.MANAGER
