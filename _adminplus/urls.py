from django.urls import path
from . import views

from django_silly_adminplus.config import SILLY_ADMINPLUS as conf

# the url patterns are automaticaly included in the main urls.py within the namespace 'adminplus',
# do not change this.

urlpatterns = [
    path(conf['DSAP_PREFIX'] + 'adminplus/', views.adminplus, name='adminplus'),
    path(conf['DSAP_PREFIX'] + 'create_user/', views.create_user, name='adminplus_create_user'),
]
