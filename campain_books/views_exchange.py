from django.db.models import Q

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView

from .models import (
    Collection,
    CollectionItem,
    CollectionPC,
    Campain,
    Item,
    PlayerCharacter,
    )
from .serializers_exchange import (
    CampainExchangesMiniSerializer,
)


class exchangesLoading(GenericAPIView):
    """Serves the exchangeable objects: campains and collections"""
    permission_classes = [IsAuthenticated]
    serializer_class = CampainExchangesMiniSerializer

    def get(self, request):
        user = request.user
        # campains
        campains = Campain.objects.filter(game_master=user).order_by('game')

        campain_serializer = CampainExchangesMiniSerializer(
            campains, many=True, context={'request': request}
            )

        return Response({'campains': campain_serializer.data})
