# from django.db.models import Q
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView

from .helpers import check_before_exchanges

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
    CollectionsFullSerializer
)
from .serializers import (
    CampainItemsSerializer,
)
from .permissions import IsSubscriber


class exchangesLoading(GenericAPIView):
    """Serves the exchangeable objects: campains and collections"""
    permission_classes = [IsAuthenticated, IsSubscriber]
    serializer_class = CampainExchangesMiniSerializer

    def get(self, request):
        user = request.user
        # campains
        campains = Campain.objects.filter(game_master=user).order_by('-table', '-game', '-title')

        campain_serializer = CampainExchangesMiniSerializer(
            campains, many=True, context={'request': request}
            )
        # collections
        collections = Collection.objects.filter(author=user).order_by('-game', '-title')
        collection_serializer = CollectionExchangesMiniSerializer(
            collections, many=True, context={'request': request}
        )

        # favorites
        favorites = Collection.objects.filter(fav_users=user).order_by('-game', '-title')
        favorites_serializer = CollectionExchangesMiniSerializer(
            favorites, many=True, context={'request': request}
        )

        return Response({
            'campains': campain_serializer.data,
            'collections': collection_serializer.data,
            'favorites': favorites_serializer.data,
            })


class ApplyExchanges(GenericAPIView):
    permission_classes = [IsAuthenticated, IsSubscriber]

    @transaction.atomic
    def post(self, request):
        exchanges = request.data['exchanges']
        user = request.user
        a_type = exchanges['a_type']
        b_type = exchanges['b_type']
        if a_type not in ['campain', 'collection'] or b_type not in ['campain', 'collection']:
            return Response(
                {'message': 'requested source does not exist'},
                400
                )
        try:
            if exchanges['a_type'] == 'campain':
                source_a = get_object_or_404(Campain, id=exchanges['a_id'])
            if exchanges['a_type'] == 'collection':
                source_a = get_object_or_404(Collection, id=exchanges['a_id'])
            if exchanges['b_type'] == 'campain':
                source_b = get_object_or_404(Campain, id=exchanges['b_id'])
            if exchanges['b_type'] == 'collection':
                source_b = get_object_or_404(Collection, id=exchanges['b_id'])
        except Campain.DoesNotExist or Collection.DoesNotExist:
            return Response(
                {'message': 'requested source does not exist'},
                400
                )

        exchanges_are_valid = check_before_exchanges(user, source_a, source_b, exchanges)
        if not exchanges_are_valid:
            return Response(
                {'message': 'requested exchanges are  not allowed'},
                400
                )

        created_copies = []

        for id in exchanges['from_a']['items']:
            try:
                if a_type == 'campain':
                    item = get_object_or_404(Item, id=id)
                if a_type == 'collection':
                    item = get_object_or_404(CollectionItem, id=id)
            except CollectionItem.DoesNotExist or Item.DoesNotExist:
                return Response(
                    {'message': 'requested item does not exist'},
                    400
                    )
            if b_type == 'campain':
                copy = Item(
                    campain=source_b,
                    name=item.name,
                    image_url=item.image_url,
                    type=item.type,
                    data_pc=item.data_pc,
                    data_gm=item.data_gm,
                    )
            if b_type == 'collection':
                copy = CollectionItem(
                    collection=source_b,
                    name=item.name,
                    image_url=item.image_url,
                    type=item.type,
                    data_pc=item.data_pc,
                    data_gm=item.data_gm,
                )
            created_copies.append(copy)

        for id in exchanges['from_a']['pcs']:
            try:
                if a_type == 'campain':
                    pc = get_object_or_404(PlayerCharacter, id=id)
                if a_type == 'collection':
                    pc = get_object_or_404(CollectionPC, id=id)
            except CollectionPC.DoesNotExist or PlayerCharacter.DoesNotExist:
                return Response(
                    {'message': 'requested pc does not exist'},
                    400
                    )
            if b_type == 'campain':
                copy = PlayerCharacter(
                    campain=source_b,
                    name=pc.name,
                    image_url=pc.image_url,
                    data_pc=pc.data_pc,
                    data_player=pc.data_player,
                    data_gm=pc.data_gm,
                    )
            if b_type == 'collection':
                copy = CollectionPC(
                    collection=source_b,
                    name=pc.name,
                    image_url=pc.image_url,
                    data_pc=pc.data_pc,
                    data_player=pc.data_player,
                    data_gm=pc.data_gm,
                )
            created_copies.append(copy)

        for id in exchanges['from_b']['items']:
            try:
                if b_type == 'campain':
                    item = get_object_or_404(Item, id=id)
                if b_type == 'collection':
                    item = get_object_or_404(CollectionItem, id=id)
            except CollectionItem.DoesNotExist or Item.DoesNotExist:
                return Response(
                    {'message': 'requested item does not exist'},
                    400
                    )
            if a_type == 'campain':
                copy = Item(
                    campain=source_a,
                    name=item.name,
                    image_url=item.image_url,
                    type=item.type,
                    data_pc=item.data_pc,
                    data_gm=item.data_gm,
                    )
            if a_type == 'collection':
                copy = CollectionItem(
                    collection=source_a,
                    name=item.name,
                    image_url=item.image_url,
                    type=item.type,
                    data_pc=item.data_pc,
                    data_gm=item.data_gm,
                )
            created_copies.append(copy)

        for id in exchanges['from_b']['pcs']:
            try:
                if b_type == 'campain':
                    pc = get_object_or_404(PlayerCharacter, id=id)
                if b_type == 'collection':
                    pc = get_object_or_404(CollectionPC, id=id)
            except CollectionPC.DoesNotExist or PlayerCharacter.DoesNotExist:
                return Response(
                    {'message': 'requested pc does not exist'},
                    400
                    )
            if a_type == 'campain':
                copy = PlayerCharacter(
                    campain=source_a,
                    name=pc.name,
                    image_url=pc.image_url,
                    data_pc=pc.data_pc,
                    data_player=pc.data_player,
                    data_gm=pc.data_gm,
                    )
            if a_type == 'collection':
                copy = CollectionPC(
                    collection=source_a,
                    name=pc.name,
                    image_url=pc.image_url,
                    data_pc=pc.data_pc,
                    data_player=pc.data_player,
                    data_gm=pc.data_gm,
                )
            created_copies.append(copy)

        for copy in created_copies:
            copy.save()

        if a_type == 'campain':
            serializer_a = CampainItemsSerializer(source_a, context={'request': request})
        if a_type == 'collection':
            serializer_a = CollectionsFullSerializer(source_a)
        if b_type == 'campain':
            serializer_b = CampainItemsSerializer(source_b, context={'request': request})
        if b_type == 'collection':
            serializer_b = CollectionsFullSerializer(source_b)

        # return Response({'message': 'ok'})
        return Response({
            'source_a': serializer_a.data,
            'source_b': serializer_b.data
            })
