from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import Configuration
from .serializers import ConfigurationSerializer


class ConfigurationView(GenericAPIView):
    """Serves the configuration"""
    serializer_class = ConfigurationSerializer

    def get(self, request):
        configuration = Configuration.objects.first()
        serializer = ConfigurationSerializer(configuration)
        return Response(serializer.data)
