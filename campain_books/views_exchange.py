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

        collections = Collection.objects.filter(author=user).order_by('game')
        collection_serializer = CollectionExchangesMiniSerializer(
            collections, many=True, context={'request': request}
        )

        return Response({
            'campains': campain_serializer.data,
            'collections': collection_serializer.data,
            })


# class CollectionDetails(GenericAPIView):
#     """Serves the details of a collection"""
#     permission_classes = [IsAuthenticated]
#     serializer_class = CollectionItemSerializer

#     def get(self, request):
#         user = request.user
#         pk = request.GET.get('pk')
#         if not Collection.objects.filter(id=pk).exists():
#             return Response({'error': 'Not found'}, status=404)

#         collection = Collection.objects.get(pk=pk)
#         if collection.author != user:
#             return Response({'error': 'Not authorized'}, status=403)

#         collection_serializer = CollectionItemSerializer(
#             collection, context={'request': request}
#         )

#         return Response(collection_serializer.data)