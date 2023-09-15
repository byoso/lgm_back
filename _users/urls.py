from django.urls import path
from . import views


urlpatterns = [
        path(f'token/login/', views.LoginWithAuthToken.as_view(), name="token_login"),
]
