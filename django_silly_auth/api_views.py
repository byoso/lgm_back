from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect

from django_silly_auth.utils import Color as c
from django_silly_auth.serializers import UserSerializer
from django_silly_auth.config import SILLY_AUTH_SETTINGS
from django_silly_auth.utils import (
    send_password_reset_email,
    send_confirm_email
)

User = get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])
def confirm_email(request, token):
    user = User.verify_jwt_token(token)
    if user:
        user.confirmed = True
        user.save()
        if SILLY_AUTH_SETTINGS["LOGIN_REDIRECT"]:
            return redirect(SILLY_AUTH_SETTINGS["LOGIN_REDIRECT"])
        return Response({'success': 'account confirmed'})
    return Response({'error': 'invalid token'})


class UserView(APIView):
    permission_classes = []

    def get(self, request, format=None):
        if SILLY_AUTH_SETTINGS["GET_ALL_USERS"]:
            print(f"{c.warning}WARNING: SILLY_AUTH[\"GET_ALL_USERS\"] == True, set it to False in production{c.end}")
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response({'users': serializer.data})
        else:
            return Response({'error': 'Not allowed'})

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            serializer = UserSerializer(user)

            if SILLY_AUTH_SETTINGS["EMAIL_SEND_ACCOUNT_CONFIRM_LINK"]:
                send_confirm_email(request, user)

            return Response({'user': serializer.data})
        else:
            return Response({'error': serializer.errors})
