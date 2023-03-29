import jwt
from time import time

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db import models
from django.contrib.auth import get_user_model


class SillyAuthUserMixin(models.Model):

    new_email = models.EmailField(blank=True, null=True, unique=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        abstract = True

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
        return get_object_or_404(get_user_model(), id=pk)
