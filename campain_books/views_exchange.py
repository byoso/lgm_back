
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

from .serializers import (
    CollectionsSerializer,
    CollectionItemSerializer,
    CollectionPCSerializer,
    CampainIdSerializer,
    ItemsSerializer,
    PlayerCharacterSerializer,
    CampainItemsSerializer,
)


class exchangeObjects(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CampainIdSerializer

    def get_exchangables(self, request):
        pass
