from django.urls import path

from . import views

urlpatterns = [
    path('articles/', views.HomeArticleViews.as_view(), name='articles'),

]
