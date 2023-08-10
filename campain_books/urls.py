
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import (
    views,
    views_collections as vc,
    views_exchange as ve,
    views_rating as vr,
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

    path('switch_guest_GM/', views.switch_guest_GM, name='switch_guest_GM'),
    path('switch_GM_owner/', views.switch_GM_owner, name='switch_GM_owner'),
    path('switch_end_campain/', views.switch_end_campain, name='switch_end_campain'),

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
    path('shared_collections/', vc.SharedCollections.as_view(), name='shared_collections'),
    path('collection/favorite_collection/', vc.favorite_collection, name='favorite_collection'),
    path(
        'create_campain_from_collection/',
        vc.create_campain_from_collection,
        name='create_campain_from_collection'),

    path('exchanges_loading/', ve.exchangesLoading.as_view(), name='exchanges_loading'),
    path('apply_exchanges/', ve.ApplyExchanges.as_view(), name='apply_exchanges'),

    path('ratings/', vr.Ratings.as_view(), name='ratings'),

    # subscriptions
    path('subscriptions/', include('subscriptions.urls')),
]
