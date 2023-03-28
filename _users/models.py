import uuid
import jwt
from time import time

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # TODO: Ajouter des validateurs avec et sans @
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    def get_jwt_token(self, expires_in=600):
        token = jwt.encode(
            {'id': str(self.id), 'exp': time() + expires_in},
            settings.SECRET_KEY, algorithm='HS256'
        )
        return token

    @staticmethod
    def verify_jwt_token(token):
        try:
            pk = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256'])['id']
        except Exception as e:
            print("Token error:", e)
            return None
        return get_object_or_404(User, id=pk)
