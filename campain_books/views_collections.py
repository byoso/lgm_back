from datetime import date

from django.db.models import Q
from django.db import transaction

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView

from .pagination import CollectionsPagination

from .models import (
    Table,
    Campain,
    Item,
    PlayerCharacter,
    Collection,
    CollectionItem,
    CollectionPC,
    Rating,
)

from .serializers import (
    TableMiniSerializer,
    )
from .serializers_collections import (
    CollectionsSerializer,
    CollectionItemSerializer,
    CollectionPCSerializer
    )

from subscriptions.permissions import IsSubscriber


class SharedCollections(GenericAPIView):
    """Responds to the research of a collection by title, author or game"""
    permission_classes = [IsAuthenticated, IsSubscriber]
    pagination_class = CollectionsPagination
    serializer_class = CollectionsSerializer

    def get(self, request):
        search_by = request.GET.get('search_by', None)
        language = request.GET.get('language', 'fr')
        if search_by == 'title':
            search_text = request.GET.get('search_text', None)
            collections = Collection.objects.filter(
                is_shared=True,
                title__icontains=search_text,
            )
        elif search_by == 'author':
            search_text = request.GET.get('search_text', None)
            collections = Collection.objects.filter(
                is_shared=True,
                author__username__icontains=search_text,
            )
        elif search_by == 'game':
            search_text = request.GET.get('search_text', None)
            collections = Collection.objects.filter(
                is_shared=True,
                game__icontains=search_text,
            )
        else:
            return Response({'message': 'search_by is required'}, status=400)
        if search_text == '':
            collections = Collection.objects.filter(is_shared=True)
        if request.GET.get('language', None) != 'all':
            collections = collections.filter(language=language)
        if request.GET.get('only_officials', None) == 'true':
            collections = collections.filter(is_official=True)

        page = self.paginate_queryset(collections)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data  # pagination data
        else:
            serializer = self.get_serializer(collections, many=True)
            data = serializer.data
        return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSubscriber])
@transaction.atomic
def create_campain_from_collection(request):
    """Create a campain from a collection
    requires collection_id, table_id and some datas
    """
    user = request.user
    if not user.is_subscriber:
        return Response({'message': 'you need to be a subscriber'}, 403)
    if not Collection.objects.filter(id=request.data['collection_id']).exists():
        return Response({'message': 'collection_id is required'}, 400)
    collection = Collection.objects.get(id=request.data['collection_id'])
    if not collection.is_shared and collection.author != user:
        return Response({'message': 'This collection is not shared'}, 403)
    table_id = request.data['table_id']
    if not Table.objects.filter(Q(id=table_id) & (Q(owners=user) | Q(game_masters=user))).exists():
        return Response({'message': 'you cant modify this table'}, 403)

    # create the campain
    campain = Campain.objects.create(
        title=collection.title,
        description=collection.description,
        table=Table.objects.get(id=table_id),
        game_master=user,
        # parent_collection=collection,
        is_copy_free=collection.is_copy_free,
        language=collection.language,
        image_url=collection.image_url,
        game=collection.game,
        is_official=collection.is_official,
        official_url=collection.official_url,
        parent_collection=collection,
    )
    # create the items
    for item in collection.items.all():
        campain_item = Item.objects.create(
            campain=campain,
            name=item.name or '',
            image_url=item.image_url or '',
            data_pc=item.data_pc or '',
            data_gm=item.data_gm or '',
            type=item.type or 'MEMO',
        )
        campain.items.add(campain_item)
    # create the pcs
    for pc in collection.pcs.all():
        campain_pc = PlayerCharacter.objects.create(
            campain=campain,
            name=pc.name or '',
            image_url=pc.image_url or '',
            data_pc=pc.data_pc or '',
            data_player=pc.data_player or '',
            data_gm=pc.data_gm or '',
        )
        campain.pcs.add(campain_pc)
    campain.parent_collection = collection
    campain.save()
    return Response({'message': 'new campain created'})


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def favorite_collection(request):
    if request.method in ['POST', 'DELETE']:
        if not Collection.objects.filter(id=request.data['collection_id']).exists():
            raise ValidationError({'message': 'collection_id is required'})
    user = request.user
    if request.method == 'GET':
        collections = Collection.objects.filter(
            Q(fav_users=user) & Q(is_shared=True)
            )
        serializer = CollectionsSerializer(collections, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.is_subscriber:
            return Response({'message': 'Subscribers only'}, 403)
        collection = Collection.objects.get(id=request.data['collection_id'])
        if collection.fav_users.filter(id=user.id).exists():
            return Response({'message': 'already in favs'})
        collection.fav_users.add(user)
        collection.save()
        return Response({'message': 'added to favs'})
    elif request.method == 'DELETE':
        collection = Collection.objects.get(id=request.data['collection_id'])
        if collection.fav_users.filter(id=user.id).exists():
            collection.fav_users.remove(user)
            collection.save()
            return Response({'message': 'removed from favs'})
        return Response({'message': 'not in favs'})
    return Response({'message': 'Something gone wrong'}, 400)


@api_view(['POST', 'GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def collections_crud(request):
    if request.method == 'POST':
        if not request.user.is_subscriber:
            return Response({'message': 'Subscribers only'}, 403)
        user = request.user
        date_now = date.today()
        history = f"{date_now} - Created by {user.username}"
        collection = Collection.objects.create(
            author=user,
            title="New Collection",
            language="en",
            history=history,
            image_url="",
        )
        Rating.objects.create(
            collection=collection
        )
        serializer = CollectionsSerializer(collection, context={'request': request})
        return Response(serializer.data)

    if request.method == 'GET':
        user = request.user
        collections = Collection.objects.filter(author=user)
        collections_serializer = CollectionsSerializer(collections, many=True, context={'request': request})
        tables = Table.objects.filter(Q(owners=user) | Q(game_masters=user))
        tables_serializer = TableMiniSerializer(tables, many=True)
        return Response({
            'collections': collections_serializer.data,
            'tables': tables_serializer.data
            })

    if request.method == 'DELETE':
        if not request.user.is_subscriber:
            return Response({'message': 'Subscribers only'}, 403)
        if 'id' not in request.data:
            return Response({'message': 'id is required'}, status=400)
        id = request.data['id']
        if not Collection.objects.filter(id=id).exists():
            return Response({'message': 'ressource not found'}, status=404)
        collection = Collection.objects.get(id=id)
        if collection.author != request.user:
            return Response({'message': 'you are not the owner of this ressource'}, status=403)
        collection.delete()
        return Response({'message': 'ressource deleted'}, status=200)

    if request.method == 'PUT':
        if not request.user.is_subscriber:
            return Response({'message': 'Subscribers only'}, 403)
        if 'id' not in request.data:
            return Response({'message': 'id is required'}, status=400)
        id = request.data['id']
        if not Collection.objects.filter(id=id).exists():
            return Response({'message': 'ressource not found'}, status=404)
        collection = Collection.objects.get(id=id)
        if collection.author != request.user:
            return Response({'message': 'you are not the owner of this ressource'}, status=403)

        # Handle the items actions
        if 'items_to_create' in request.data:
            items_to_create = request.data['items_to_create']
            for item_id in items_to_create:
                item = items_to_create[item_id]
                item['collection'] = id
                serializer = CollectionItemSerializer(data=item, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=400)

        if 'items_to_delete' in request.data:
            items_to_delete = request.data['items_to_delete']
            for item_id in items_to_delete:
                if not CollectionItem.objects.filter(id=item_id).exists():
                    return Response({'message': 'ressource not found'}, status=404)
                item = CollectionItem.objects.get(id=item_id)
                if item.collection != collection:
                    return Response({'message': 'you are not the owner of this ressource'}, status=403)
                item.delete()

        if 'items_to_update' in request.data:
            items_to_update = request.data['items_to_update']
            for item_id in items_to_update:
                if not CollectionItem.objects.filter(id=item_id).exists():
                    return Response({'message': 'ressource not found'}, status=404)
                old_item = CollectionItem.objects.get(id=item_id)
                if old_item.collection != collection:
                    return Response({'message': 'you are not the owner of this ressource'}, status=403)
                item = items_to_update[item_id]
                if 'name' in item:
                    old_item.name = item['name'].strip()
                if 'description' in item:
                    old_item.description = item['description'].strip()
                if 'image_url' in item:
                    old_item.image_url = item['image_url']
                if 'data_pc' in item:
                    old_item.data_pc = item['data_pc'].strip()
                if 'data_gm' in item:
                    old_item.data_gm = item['data_gm'].strip()
                if 'type' in item:
                    old_item.type = item['type']
                old_item.save()

        # handle the pcs
        if 'pcs_to_create' in request.data:
            pcs_to_create = request.data['pcs_to_create']
            for pc_id in pcs_to_create:
                pc = pcs_to_create[pc_id]
                pc['collection'] = id
                serializer = CollectionPCSerializer(data=pc, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=400)

        if 'pcs_to_delete' in request.data:
            pcs_to_delete = request.data['pcs_to_delete']
            for pc_id in pcs_to_delete:
                if not CollectionPC.objects.filter(id=pc_id).exists():
                    return Response({'message': 'ressource not found'}, status=404)
                pc = CollectionPC.objects.get(id=pc_id)
                if pc.collection != collection:
                    return Response({'message': 'you are not the owner of this ressource'}, status=403)
                pc.delete()

        if 'pcs_to_update' in request.data:
            pcs_to_update = request.data['pcs_to_update']
            for pc_id in pcs_to_update:
                if not CollectionPC.objects.filter(id=pc_id).exists():
                    return Response({'message': 'ressource not found'}, status=404)
                old_pc = CollectionPC.objects.get(id=pc_id)
                if old_pc.collection != collection:
                    return Response({'message': 'you are not the owner of this ressource'}, status=403)
                pc = pcs_to_update[pc_id]
                if 'name' in pc:
                    old_pc.name = pc['name'].strip()
                if 'description' in pc:
                    old_pc.description = pc['description'].strip()
                if 'image_url' in pc:
                    old_pc.image_url = pc['image_url']
                if 'data_pc' in pc:
                    old_pc.data_pc = pc['data_pc'].strip()
                if 'data_player' in pc:
                    old_pc.data_player = pc['data_player'].strip()
                if 'data_gm' in pc:
                    old_pc.data_gm = pc['data_gm'].strip()
                old_pc.save()

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
    """Get the details of a collection, including its items and pcs
    - id is required in the request params.
    """
    id = request.GET['id']
    if not Collection.objects.filter(id=id).exists():
        return Response({'message': 'ressource not found'}, status=404)
    collection = Collection.objects.get(id=id)
    serializer = CollectionsSerializer(collection, context={'request': request})
    collection_details = serializer.data

    items_queryset = CollectionItem.objects.filter(collection=id)
    serializer = CollectionItemSerializer(items_queryset, many=True)
    items = serializer.data

    pcs_queryset = CollectionPC.objects.filter(collection=id)
    serializer = CollectionPCSerializer(pcs_queryset, many=True)
    pcs = serializer.data

    return Response({
        'collection_details': collection_details,
        'items': items,
        'pcs': pcs,
        })
