import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from django_silly_auth.mixins import SillyAuthUserMixin


class User(AbstractUser, SillyAuthUserMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # TODO: Ajouter des validateurs avec et sans @
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        unique=True,
    )
