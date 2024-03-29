import os
from rest_framework import serializers
from django.contrib.auth import get_user_model
from _adminplus.models import Configuration

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    is_subscriber = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'is_subscriber',
            'is_confirmed',
        ]

    def get_is_subscriber(self, obj):

        if Configuration.active_stripe_subscriptions:
            return obj.is_subscriber
        else:
            return True
