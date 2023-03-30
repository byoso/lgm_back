from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django_silly_auth.config import SILLY_AUTH_SETTINGS as conf

from django_silly_auth import api_views, views


urlpatterns = [
]

if conf["ALLOW_CREATE_USER_ENDPOINT"]:
    urlpatterns += [path('users/', api_views.UserView.as_view(), name='user_view')]
if conf["ALLOW_LOGIN_ENDPOINT"]:
    urlpatterns += [path('token/login/', obtain_auth_token)]
if conf["ALLOW_LOGOUT_ENDPOINT"]:
    urlpatterns += [path('token/logout/', api_views.logout_api_view, name='logout')]
if conf["ALLOW_EMAIL_CONFIRM_ENDPOINT"]:
    urlpatterns += [
        # webhook for email confirmation
        path(
            'confirm_email/<token>/',
            api_views.confirm_email,
            name='confirm_email'),
    ]
if conf["ALLOW_RESET_PASSWORD_ENDPOINT"]:
    urlpatterns += [
        # request password reset
        path(
            'password/request_reset/',
            api_views.request_password_reset,
            name='request_password_reset'
        ),
        path(
            conf["RESET_PASSWORD_ENDPOINT"] + '<token>/',
            views.reset_password,
            name='reset_password'
        ),
        path(
            'password/reset/done/',
            views.password_reset_done,
            name='reset_password_done'
        )
    ]