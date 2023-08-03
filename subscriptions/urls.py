from django.urls import path
from django.db.models.signals import post_save, post_delete
from . import views

from django_silly_stripe.models import (
    Subscription
)
from django_silly_stripe.views import (
    get_plans,
)
from django_silly_stripe.helpers import (
    get_subscription_user,
    get_user_subscriptions,
)


urlpatterns = [
    path('plans/', get_plans, name='get_plans'),
]


# signal on subscription change
def on_subscription_change(sender, instance, **kwargs):
    subscription = instance
    user = get_subscription_user(subscription)
    if get_user_subscriptions(user):
        user.is_subscriber = True
    else:
        user.is_subscriber = False
    user.save()


post_save.connect(on_subscription_change, sender=Subscription)
post_delete.connect(on_subscription_change, sender=Subscription)
