from django.urls import path
from django.db.models.signals import post_save, pre_delete
from . import views

from django_silly_stripe.models import (
    Subscription
)
from django_silly_stripe.views import (
    get_plans,
)


urlpatterns = [
    path('plans/', get_plans, name='get_plans'),
]


# signal on subscription update
def on_subscription_update(sender, instance, created, **kwargs):
    print("=== Signal: on_subscription_update ===")
    print("instance: ", instance)
    print("created: ", created)
    print("kwargs: ", kwargs)


def on_subscription_delete(sender, instance, **kwargs):
    print("=== Signal: on_subscription_delete ===")
    print("instance: ", instance)
    print("kwargs: ", kwargs)


post_save.connect(on_subscription_update, sender=Subscription)
pre_delete.connect(on_subscription_delete, sender=Subscription)