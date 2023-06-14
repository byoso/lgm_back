
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import (
    views,
    views_collections as vc
    )

router = DefaultRouter()
router.register('tables', views.TableViewSet, basename='tables')
router.register('campains', views.CampainViewSet, basename='campains')


urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('get_tables_as_owner/', views.get_tables_as_owner, name='get_tables_as_owner'),
    path('get_tables_as_user/', views.get_tables_as_user, name='get_tables_as_user'),
    path('get_table_datas/', views.get_table_datas, name='get_table_datas'),
    path('switch_guest_owner/', views.switch_guest_owner, name='switch_guest_owner'),
    path('get_campains_for_table/', views.get_campains_for_table, name='get_campains_for_table'),
    path('update_campain/', views.update_campain, name='update_campain'),
    path('items/create/', views.create_item, name='create_item'),
    path('items/update/', views.update_item, name='update_item'),
    path('items/delete/', views.delete_item, name='delete_item'),
    path('pc/create/', views.create_pc, name='create_pc'),
    path('pc/update/', views.update_pc, name='update_pc'),
    path('pc/delete/', views.delete_pc, name='delete_pc'),

    path('collections_crud/', vc.collections_crud, name='collections_crud'),
    path('collection/', vc.collection_detail, name='collection'),
]
