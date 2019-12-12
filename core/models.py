from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(object):
    PELAYAN = 1
    KASIR = 2
    MANAGER = 99

    ROLE_CHOICES = (
        (PELAYAN, 'Pelayan'),
        (KASIR, 'Kasir'),
        (MANAGER, 'Manager'),
    )


class User(AbstractUser):
    role = models.PositiveSmallIntegerField(choices=Role.ROLE_CHOICES)
