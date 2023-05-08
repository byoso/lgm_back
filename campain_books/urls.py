from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from . import views

urlpatterns = [
    path('tables/create/', views.create_table, name='create_table'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('get_tables_as_owner/', views.get_tables_as_owner, name='get_tables_as_owner'),
    path('get_tables_as_user/', views.get_tables_as_user, name='get_tables_as_user'),
    path('get_table_datas/', views.get_table_datas, name='get_table_datas'),
]
