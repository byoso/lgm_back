from rest_framework import serializers

from .models import Configuration


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = (
            'open_subscriptions',
            'active_stripe_subscriptions',
            'active_stripe_portal',
            'active_tip_me',
            )
        read_only_fields = (
            'open_subscriptions',
            'active_stripe_subscriptions',
            'active_stripe_portal',
            'active_tip_me',
            )
