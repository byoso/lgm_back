from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import redirect

from django_silly_auth.serializers import UserSerializer
from django_silly_auth.config import SILLY_AUTH_SETTINGS as conf
from django_silly_auth.utils import (
    send_password_reset_email,
    send_confirm_email
)
from django_silly_auth.utils import warning

User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])
def confirm_email(request, token):
    """Recieves the token given by email and confirms the user's account"""
    user = User.verify_jwt_token(token)
    if user:
        user.confirmed = True
        user.save()
        if conf["LOGIN_REDIRECT"]:
            return redirect(conf["LOGIN_REDIRECT"])
        return Response({'success': 'account confirmed'})
    return Response({'error': 'invalid token'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_api_view(request):
    """Destroys the auth token"""
    request.user.auth_token.delete()
    return Response({'success': 'logged out, token destroyed'})


@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    """Sends an email to the user with a link to reset their password"""
    print(request.data["credential"])
    credential = request.data.get('credential')
    if not credential:
        return Response({'error': 'no credential provided'})
    if "@" in credential:
        user = User.objects.filter(email=credential).first()
    else:
        user = User.objects.filter(username=credential).first()
    if user:
        send_password_reset_email(request, user)
        return Response({'success': 'email sent for password reset'})
    return Response({'error': 'user not found'})


@api_view(['GET'])
@permission_classes([AllowAny])
def reset_password(request, token):
    """Recieves the token given by email and confirms the user's account"""
    user = User.verify_jwt_token(token)
    if user:
        if not user.confirmed:
            user.confirmed = True
            user.save()
        if conf["PASSWORD_RESET_REDIRECT"]:
            return redirect(conf["PASSWORD_RESET_REDIRECT"])
        return Response({'success': 'logged in from email'})
    return Response({'error': 'invalid token'})


class UserView(APIView):
    permission_classes = []

    def get(self, request, format=None):
        if conf["GET_ALL_USERS"]:
            warning(
                "WARNING: SILLY_AUTH[\"GET_ALL_USERS\"] "
                "== True, set it to False in production."
            )
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

            if conf["EMAIL_SEND_ACCOUNT_CONFIRM_LINK"]:
                send_confirm_email(request, user)

            return Response({'user': serializer.data})
        else:
            return Response({'error': serializer.errors})
