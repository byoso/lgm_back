import uuid
import jwt
from time import time

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

from .validators import validate_email, validate_username
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
        validators=[validate_username]
    )
    email = models.EmailField(
        unique=True,
        validators=[validate_email]
    )
