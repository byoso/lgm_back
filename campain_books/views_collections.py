from datetime import datetime, date

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .models import (
    Collection,
    CollectionItem,
    CollectionPC,
)

from .permissions import IsOwner, IsGuestOrOwner
from .helpers import is_game_master, is_player
from .serializers_collections import (
    CollectionsSerializer,
    CollectionItemSerializer
    )


@api_view(['POST', 'GET', 'DELETE', 'PUT'])
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
            image_url="",
        )
        serializer = CollectionsSerializer(collection)
        return Response(serializer.data)

    if request.method == 'GET':
        user = request.user
        collections = Collection.objects.filter(author=user)
        serializer = CollectionsSerializer(collections, many=True)
        return Response(serializer.data)

    if request.method == 'DELETE':
        if 'id' not in request.data:
            return Response({'message': 'id is required'}, status=400)
        id = request.data['id']
        if not Collection.objects.filter(id=id).exists():
            return Response({'message': 'ressource not found'}, status=404)
        collection = Collection.objects.get(id=id)
        collection.delete()
        return Response({'message': 'ressource deleted'}, status=200)

    if request.method == 'PUT':
        if 'id' not in request.data:
            return Response({'message': 'id is required'}, status=400)
        id = request.data['id']
        if not Collection.objects.filter(id=id).exists():
            return Response({'message': 'ressource not found'}, status=404)

        # Handle the items actions
        if 'items_to_create' in request.data:
            print("===Items to create: ", request.data['items_to_create'])
            items_to_create = request.data['items_to_create']
            for item_id in items_to_create:
                item = items_to_create[item_id]
                item['collection'] = id
                print(item)
                serializer = CollectionItemSerializer(data=item, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=400)

        if 'items_to_delete' in request.data:
            print("===Items to delete: ", request.data['items_to_delete'])
            items_to_delete = request.data['items_to_delete']
            for item_id in items_to_delete:
                if not CollectionItem.objects.filter(id=item_id).exists():
                    return Response({'message': 'ressource not found'}, status=404)
                item = CollectionItem.objects.get(id=item_id)
                item.delete()

        if 'items_to_update' in request.data:
            print("===Items to update: ", request.data['items_to_update'])
            items_to_update = request.data['items_to_update']
            for item_id in items_to_update:
                if not CollectionItem.objects.filter(id=item_id).exists():
                    return Response({'message': 'ressource not found'}, status=404)
                old_item = CollectionItem.objects.get(id=item_id)
                item = items_to_update[item_id]
                print("===item_to_update: ", item)
                if 'name' in item:
                    old_item.name = item['name']
                if 'description' in item:
                    old_item.description = item['description']
                if 'image_url' in item:
                    old_item.image_url = item['image_url']
                if 'data_pc' in item:
                    old_item.data_pc = item['data_pc']
                if 'data_gm' in item:
                    old_item.data_gm = item['data_gm']
                if 'type' in item:
                    old_item.type = item['type']
                old_item.save()
                # serializer = CollectionItemSerializer(data=item_to_update, context={'request': request})
                # if serializer.is_valid():
                #     serializer.save()
                # else:
                #     return Response(serializer.errors, status=400)

        # Handle the collection
        collection = Collection.objects.get(id=id)
        serializer = CollectionsSerializer(collection, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def collection_detail(request):
    id = request.GET['id']
    if not Collection.objects.filter(id=id).exists():
        return Response({'message': 'ressource not found'}, status=404)
    collection = Collection.objects.get(id=id)
    serializer = CollectionsSerializer(collection)
    collection_details = serializer.data

    items_queryset = CollectionItem.objects.filter(collection=id)
    serializer = CollectionItemSerializer(items_queryset, many=True)
    items = serializer.data

    return Response({
        'collection_details': collection_details,
        'items': items,

        })
