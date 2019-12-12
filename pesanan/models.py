from datetime import date
from django.db import models
from core import models as core_models

# Create your models here.


STATUS_CHOICE = (
    ('ready', 'Ready'),
    ('sold_out', 'Sold Out'),
)


class Makanan(models.Model):
    nama = models.CharField(max_length=50)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default='ready')
    harga = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Minuman(models.Model):
    nama = models.CharField(max_length=50)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default='ready')
    harga = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Pesanan(models.Model):
    nomor = models.IntegerField(default=0)
    nomor_meja = models.IntegerField()
    kode_pesanan = models.CharField(max_length=15, null=True)
    lunas = models.BooleanField(default=False)
    bayar = models.FloatField(default=0.00)
    kembalian = models.FloatField(default=0.00)
    pelayan = models.ForeignKey(core_models.User, related_name='pesanan',
                                on_delete=models.SET_NULL, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def approve(self):
        self.lunas = True
        self.save()

    def generate_kode(self):
        nomor = Pesanan.objects.filter(
            created__year=date.today().year, created__month=date.today().month
        ).order_by('nomor').last()
        if nomor is not None:
            nomor = nomor.nomor + 1
            self.nomor = nomor
            self.save()
            return f'ERP{date.today().day}{date.today().month}{date.today().year}-{nomor:03d}'
        else:
            self.nomor = self.nomor + 1
            self.save()
            return f'ERP{date.today().day}{date.today().month}{date.today().year}-{self.nomor:03d}'

    def kode(self):
        self.kode_pesanan = self.generate_kode()
        self.save()


class DaftarPesanan(models.Model):
    pesanan = models.ForeignKey(
        Pesanan, related_name='daftar_pesanan', on_delete=models.SET_NULL,
        null=True)
    makanan = models.ForeignKey(
        Makanan, related_name='daftar_pesanan_makanan', on_delete=models.CASCADE,
        null=True)
    makanan_jumlah = models.IntegerField(default=1)
    minuman = models.ForeignKey(
        Minuman, related_name='daftar_pesanan_minuman', on_delete=models.CASCADE,
        null=True)
    minuman_jumlah = models.IntegerField(default=1)
