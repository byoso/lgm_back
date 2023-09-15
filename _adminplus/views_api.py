from django.http import JsonResponse
from rest_framework.generics import GenericAPIView

from .models import Configuration

class ConfigurationView(GenericAPIView):
    """Serves the configuration"""

    def get(self, request):
        return JsonResponse({
            'open_subscriptions': Configuration.open_subscriptions,
            'active_stripe_subscriptions': Configuration.active_stripe_subscriptions,
            'active_stripe_portal': Configuration.active_stripe_portal,
            'active_tip_me': Configuration.active_tip_me,
        })
