from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _

from django_silly_auth.mixins import SillyAuthUserMixin


class User(
    SillyAuthUserMixin,
    AbstractUser
        ):
    is_subscriber = models.BooleanField(default=False)

    fav_collections = models.ManyToManyField(
        to='campain_books.Collection',
        related_name='fav_users',
        blank=True,
    )

    def __str__(self):
        return self.username
