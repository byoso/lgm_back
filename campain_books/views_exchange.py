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
    CollectionExchangesMiniSerializer,
)
from .serializers_collections import (
    CollectionItemSerializer,
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
        # collections
        collections = Collection.objects.filter(author=user).order_by('game')
        collection_serializer = CollectionExchangesMiniSerializer(
            collections, many=True, context={'request': request}
        )

        # favorites
        favorites = Collection.objects.filter(fav_users=user).order_by('game')
        favorites_serializer = CollectionExchangesMiniSerializer(
            favorites, many=True, context={'request': request}
        )

        return Response({
            'campains': campain_serializer.data,
            'collections': collection_serializer.data,
            'favorites': favorites_serializer.data,
            })
