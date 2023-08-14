from rest_framework import serializers

from .models import Configuration


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ('open_subscriptions', )
        read_only_fields = ('open_subscriptions', )
