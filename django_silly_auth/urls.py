from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django_silly_auth.config import SILLY_AUTH_SETTINGS as conf

from django_silly_auth import api_views


urlpatterns = [
    # create user, get all users (dev, not prod)
    path('users/', api_views.UserView.as_view(), name='user_view'),
    # webhook for email confirmation
    path(
        'confirm_email/<token>/',
        api_views.confirm_email,
        name='confirm_email'),

    # login
    path('token/login/', obtain_auth_token),
    # destroy token (logout)

    # email send account confirmation link
    # verify account

    # email send password reset link
    # reset password

]
