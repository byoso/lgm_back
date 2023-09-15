from rest_framework import serializers
from django.contrib.auth import get_user_model

from _adminplus.models import Configuration as AdminplusConfig

User = get_user_model()

config = AdminplusConfig.objects.first()

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
        try:
            if config.active_stripe_subscriptions:
                return obj.is_subscriber
            else:
                return True
        except Exception as e:
            print("==== exception:", e)
            return True
