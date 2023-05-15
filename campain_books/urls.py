
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views
from .populate import populate

router = DefaultRouter()
router.register('tables', views.TableViewSet, basename='tables')
router.register('campains', views.CampainViewSet, basename='campains')


urlpatterns = [
    path('', include(router.urls)),
    # path('tables/create/', views.create_table, name='create_table'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('get_tables_as_owner/', views.get_tables_as_owner, name='get_tables_as_owner'),
    path('get_tables_as_user/', views.get_tables_as_user, name='get_tables_as_user'),
    path('get_table_datas/', views.get_table_datas, name='get_table_datas'),
    path('switch_guest_owner/', views.switch_guest_owner, name='switch_guest_owner'),
    path('get_games_list/', views.get_games_list, name='get_games_list'),
]

populate()
