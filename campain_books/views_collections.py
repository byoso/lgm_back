from datetime import datetime, date

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .models import (
    Collection
)

from .permissions import IsOwner, IsGuestOrOwner
from .helpers import is_game_master, is_player
from .serializers_collections import CollectionsSerializer


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def collections_crud(request):
    if request.method == 'POST':
        user = request.user
        date_now = date.today()
        history = f"{date_now} - Created by {user.username}"
        collection = Collection.objects.create(
            author=user,
            name="New Collection",
            language="en",
            history=history,
        )
        serializer = CollectionsSerializer(collection)
        return Response(serializer.data)

    if request.method == 'GET':
        user = request.user
        collections = Collection.objects.filter(author=user)
        serializer = CollectionsSerializer(collections, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def collection_detail(request):
    print("=== request.data", request.GET)
    id = request.GET['id']
    if not Collection.objects.filter(id=id).exists():
        return Response({'message': 'ressource not found'}, status=404)
    collection = Collection.objects.get(id=id)
    serializer = CollectionsSerializer(collection)

    return Response(serializer.data)
