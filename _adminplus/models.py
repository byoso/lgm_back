import os


class Configuration:
    """Config usable for your app, change it to your liking."""
    open_subscriptions = os.environ.get('OPEN_SUBSCRIPTIONS', "0") == "1"
    active_stripe_subscriptions = os.environ.get('ACTIVE_STRIPE_SUBSCRIPTIONS', "0") == "1"
    active_stripe_portal = os.environ.get('ACTIVE_STRIPE_PORTAL', "0") == "1"
    active_tip_me = os.environ.get('ACTIVE_TIP_ME', "0") == "1"

    # Add your settings here

    def __str__(self):
        return 'Configuration (fake singleton from environ)'
