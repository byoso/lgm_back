from django.urls import path
from . import views

urlpatterns = [
    path('create-checkout-session/', views.CreateCheckoutSession.as_view(), name='create-checkout-session'),
    path('webhook/', views.Webhook.as_view(), name='webhook')
]
