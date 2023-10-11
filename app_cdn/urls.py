from django.urls import path
from django.conf import settings

from . import views

app_name = "cdn"
urlpatterns = [
    path('cdn_home/', views.home, name='home'),
    # projects
    path('new_project/', views.new_project, name='new_project'),
    path('project/<project_id>/', views.project, name='project'),
    path('project/<project_id>/edit/', views.edit_project, name='edit_project'),
    path('project/<project_id>/delete/', views.delete_project, name='delete_project'),
    # items
    path('project/<project_id>/new_item/', views.new_item, name='new_item'),
    path('item/<item_id>/edit_item/', views.edit_item, name='edit_item'),
    path('item/<item_id>/delete_item/', views.delete_item, name='delete_item'),

]
