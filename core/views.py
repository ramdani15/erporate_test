from django.shortcuts import get_object_or_404

from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions as perms, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from . import serializers, models, pagination, permissions

User = get_user_model()


def jwt_response_handler(token, user=None, request=None):
    serializer = serializers.UserSerializer(user, context={'request': request})
    return {
        'token': token,
        'user': serializer.data
    }


class UserViewset(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = (perms.IsAuthenticated,
                          permissions.UserPermission,)
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = pagination.ResultPagination

    def get_queryset(self):
        if self.request.user.role == models.Role.MANAGER:
            queryset = User.objects.all()
        elif self.request.user.role == models.Role.KASIR:
            queryset = User.objects.exlcude(role=models.Role.MANAGER)
        else:
            queryset = User.objects.filter(role=models.Role.PELAYAN)
        return queryset

    @action(methods=['get'],
            detail=False,
            permission_classes=[perms.IsAuthenticated,
                                permissions.UserPermission, ],
            authentication_classes=[JSONWebTokenAuthentication])
    def me(self, request):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=True,
            methods=['POST'],
            permission_classes=(perms.IsAuthenticated,
                                permissions.UserPermission),
            url_path='change-password')
    def change_password(self, request, pk=None):
        user = get_object_or_404(models.User, pk=pk)
        user.change_password()
        user.set_password(request.data.get('password'))
        user.save()
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
