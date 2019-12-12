from rest_framework import permissions
from core.models import Role


class MakananPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or\
            request.user.role in [Role.KASIR]

    def has_object_permission(self, request, view, obj):
        return view.action in ['retrieve'] or\
            request.user.role in [Role.KASIR]


class PesananPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create']:
            return request.user.role == Role.PELAYAN
        return request.method in permissions.SAFE_METHODS or\
            request.user.role in [Role.KASIR, Role.PELAYAN]

    def has_object_permission(self, request, view, obj):
        if view.action in ['create']:
            return request.user.role == Role.PELAYAN
        return view.action in ['retrieve'] or\
            request.user.role == Role.KASIR or\
            request.user == obj.pelayan


class DaftarPesananPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create']:
            return request.user.role == Role.PELAYAN
        return request.method in permissions.SAFE_METHODS or\
            request.user.role in [Role.KASIR, Role.PELAYAN]

    def has_object_permission(self, request, view, obj):
        if view.action in ['create']:
            return request.user.role == Role.PELAYAN
        return view.action in ['retrieve'] or\
            request.user.role == Role.KASIR or\
            request.user == obj.pesanan.pelayan
