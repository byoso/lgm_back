
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.serializers import ValidationError

from django_silly_auth.serializers import (
    LoginSerializer,
    )

from .serializers import UserSerializer


User = get_user_model()


class LoginWithAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        """Login view modified to use email or username as credential"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        credential = serializer.validated_data['credential']
        if "@" in credential:
            user = User.objects.filter(email=credential).first()
        else:
            user = User.objects.filter(username=credential).first()
        password = serializer.validated_data['password']
        match = False
        if user:
            match = user.check_password(password)
        if match:
            if not user.is_confirmed and not user.is_superuser:
                msg = (
                    'Your account has not been confirmed yet. '
                    'Please check your inbox for a confirmation link.')
                raise ValidationError({'detail': [msg]}, code='authorization')
            token, created = Token.objects.get_or_create(user=user)
            if hasattr(user, 'last_login'):
                user.last_login = timezone.now()
                user.save()
            serializer = UserSerializer(user)
            data = {
                'auth_token': token.key,
                'user': serializer.data
            }
            return Response(
                data,
                )
        msg = 'Incorrect credentials.'
        raise ValidationError({'detail': [msg]}, code='authorization')
