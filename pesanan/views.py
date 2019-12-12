from datetime import date
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework import permissions as perms
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from . import models, permissions, serializers
from core.models import Role

# Create your views here.


class MakananViewset(viewsets.ModelViewSet):
    serializer_class = serializers.MakananSerializer
    queryset = models.Makanan.objects.all()
    permission_classes = (perms.IsAuthenticated,
                          permissions.MakananPermission)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_queryset(self):
        queryset = models.Makanan.objects.all()
        if self.request.user.role == Role.PELAYAN:
            queryset = models.Makanan.objects.filter(status='ready')
        return queryset

    @action(detail=True,
            methods=['POST'],
            permission_classes=(
                perms.IsAuthenticated,
                permissions.MakananPermission),
            authentication_classes=(JSONWebTokenAuthentication,))
    def activate(self, request, pk=None):
        obj = get_object_or_404(models.Makanan, pk=pk)
        if obj.status == "sold_out":
            obj.status = "ready"
        else:
            obj.status = "sold_out"
        obj.save()
        if obj.status == "ready":
            return Response({'message': 'Makanan Ready'},
                            status=status.HTTP_201_CREATED)
        return Response({'message': 'Makanan Sold Out'},
                        status=status.HTTP_201_CREATED)


class MinumanViewset(viewsets.ModelViewSet):
    serializer_class = serializers.MinumanSerializer
    queryset = models.Minuman.objects.all()
    permission_classes = (perms.IsAuthenticated,
                          permissions.MakananPermission)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_queryset(self):
        queryset = models.Minuman.objects.all()
        if self.request.user.role == Role.PELAYAN:
            queryset = models.Minuman.objects.filter(status='ready')
        return queryset

    @action(detail=True,
            methods=['POST'],
            permission_classes=(
                perms.IsAuthenticated,
                permissions.MakananPermission),
            authentication_classes=(JSONWebTokenAuthentication,))
    def activate(self, request, pk=None):
        obj = get_object_or_404(models.Minuman, pk=pk)
        if obj.status == "sold_out":
            obj.status = "ready"
        else:
            obj.status = "sold_out"
        obj.save()
        if obj.status == "ready":
            return Response({'message': 'Minuman Ready'},
                            status=status.HTTP_201_CREATED)
        return Response({'message': 'Minuman Sold Out'},
                        status=status.HTTP_201_CREATED)


class PesananViewset(viewsets.ModelViewSet):
    serializer_class = serializers.PesananSerializer
    queryset = models.Pesanan.objects.all()
    permission_classes = (perms.IsAuthenticated,
                          permissions.PesananPermission)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_queryset(self):
        queryset = models.Pesanan.objects.all()
        if self.request.user.role == Role.PELAYAN:
            queryset = models.Pesanan.objects.filter(pelayan=self.request.user)
        return queryset

    @action(detail=True,
            methods=['POST'],
            permission_classes=(
                perms.IsAuthenticated,
                permissions.PesananPermission),
            authentication_classes=(JSONWebTokenAuthentication,))
    def bayar(self, request, pk=None):
        bayar = request.data.get('bayar')
        obj = get_object_or_404(models.Pesanan, pk=pk)

        # kembalian
        if float(bayar) < obj.bayar:
            return Response({'message': 'Uang Kurang'},
                            status=status.HTTP_400_BAD_REQUEST)
        obj.kembalian = float(bayar) - obj.bayar
        obj.approve()

        obj.save()
        serializer = serializers.PesananSerializer(obj)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    def sum_bayar(self, obj):
        dp = models.DaftarPesanan.objects.filter(pesanan=obj)
        obj.bayar = 0
        for d in dp:
            if d.makanan is not None:
                obj.bayar += (d.makanan.harga * d.makanan_jumlah)
            else:
                obj.bayar += (d.minuman.harga * d.minuman_jumlah)
        obj.save()

    def perform_create(self, serializer):
        obj = serializer.save(pelayan=self.request.user)
        # Generate kode pesanan
        obj.kode()
        obj.save()


class DaftarPesananViewset(viewsets.ModelViewSet):
    serializer_class = serializers.DaftarPesananSerializer
    queryset = models.DaftarPesanan.objects.all()
    permission_classes = (perms.IsAuthenticated,
                          permissions.DaftarPesananPermission)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_queryset(self):
        queryset = models.DaftarPesanan.objects.all()
        pesanan = self.request.GET.get('pesanan')
        if pesanan:
            queryset = models.DaftarPesanan.objects.filter(id=pesanan)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = serializers.DaftarPesananSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        makanan = models.Makanan.objects.filter(
            id=self.request.data.get('makanan'))
        if makanan:
            makanan = models.Makanan.objects.get(
                id=self.request.data.get('makanan'))
            if makanan.status != 'ready':
                return Response({'message': 'Makanan Tidak Tersedia'},
                                status=status.HTTP_400_BAD_REQUEST)
        minuman = models.Minuman.objects.filter(
            id=self.request.data.get('minuman'))
        if minuman:
            minuman = models.Minuman.objects.get(
                id=self.request.data.get('minuman'))
            if minuman.status != 'ready':
                return Response({'message': 'Minuman Tidak Tersedia'},
                                status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        obj = serializer.save()

        # tambah total bayar
        PesananViewset.sum_bayar(self, obj.pesanan)

        obj.save()

    def perform_update(self, serializer):
        obj = serializer.save()

        # update total bayar
        PesananViewset.sum_bayar(self, obj.pesanan)

        obj.save()

    def perform_destroy(self, instance):
        PesananViewset.sum_bayar(self, instance.pesanan)
        instance.delete()
