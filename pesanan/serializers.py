from rest_framework import serializers

from . import models


class MakananSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Makanan
        fields = '__all__'


class MinumanSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Minuman
        fields = '__all__'


class DaftarPesananSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DaftarPesanan
        fields = '__all__'


class PesananSerializer(serializers.ModelSerializer):
    daftar_pesanan = DaftarPesananSerializer(many=True, read_only=True)

    class Meta:
        model = models.Pesanan
        fields = '__all__'
