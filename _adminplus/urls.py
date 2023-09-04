from django.urls import path
from . import views, views_api

# the url patterns are automaticaly included in the main urls.py within the namespace 'adminplus',
# do not change this.

urlpatterns = [
    path('dsap/adminplus/', views.adminplus, name='adminplus'),
    path('dsap/create_user/', views.create_user, name='adminplus_create_user'),
    # Custom views
    path('dsap/configuration/', views_api.ConfigurationView.as_view(), name='configuration'),
]
