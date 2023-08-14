from .models import Configuration


def subscriptions_are_open():
    return Configuration.objects.first().open_subscriptions
