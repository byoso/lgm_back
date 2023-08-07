from datetime import datetime
from pprint import pprint

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.conf import settings
from django.db import transaction

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework import viewsets

from .models import (
    Table,
    Campain,
    PlayerCharacter,
    Item,
    LANGUAGES,
    Collection,
    )
from .serializers import (
    TableSerializer,
    PlayerCharacterSerializer, CampainSerializer,
    ItemsSerializer, ItemsPCSerializer,
    CampainItemsSerializer,
    )
from .serializers_collections import (
    CollectionsSerializer,
)
from .permissions import IsOwner, IsGuestOrOwner
from .helpers import guests_create_or_not, is_game_master, is_player

from subscriptions.permissions import IsSubscriber

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tables_as_owner(request):
    tables = Table.objects.filter(owners=request.user)
    serializer = TableSerializer(tables, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tables_as_user(request):
    tables = Table.objects.filter(users=request.user)
    serializer = TableSerializer(tables, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    data = dict()
    tables_as_owner = Table.objects.filter(owners=request.user)
    serializer = TableSerializer(tables_as_owner, many=True)
    tables_as_guest = Table.objects.filter(guests=request.user)
    serializer2 = TableSerializer(tables_as_guest, many=True)
    tables_as_gm = Table.objects.filter(game_masters=request.user)
    serializer3 = TableSerializer(tables_as_gm, many=True)

    data["tables_as_owner"] = serializer.data
    data["tables_as_guest"] = serializer2.data
    data["tables_as_gm"] = serializer3.data
    pprint(data)

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_table_datas(request):
    if Table.objects.filter(id=request.GET.get('table_id')).exists():
        table = Table.objects.get(id=request.GET.get('table_id'))
        serializer = TableSerializer(table)
        return Response(serializer.data)
    raise ValidationError("This table does not exists")


class TableViewSet(viewsets.ModelViewSet):
    """Handle actions on tables but"""
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated, IsGuestOrOwner]

    def get_queryset(self):
        user = self.request.user
        return Table.objects.filter(owners=user)

    def perform_create(self, serializer):
        if not self.request.user.is_subscriber:
            return Response({"message": "Subscriber only"}, 403)
        if serializer.is_valid():
            table = serializer.save()
            table.owners.add(self.request.user)

            response_datas = guests_create_or_not(
                self.request,
                guests_list=self.request.data.get('guests'),
                table=table, message="",
                serializer=serializer,
                )
            return Response(response_datas)
        raise ValidationError(serializer.errors)

    def perform_update(self, serializer):
        if not self.request.user.is_subscriber:
            return Response({"message": "Subscriber only"}, 403)
        if serializer.is_valid():
            table = serializer.save()

            response_datas = guests_create_or_not(
                self.request,
                guests_list=self.request.data.get('guests'),
                table=table, message="",
                serializer=serializer,
                )
            return Response(response_datas)
        raise ValidationError(serializer.errors)

    def perform_destroy(self, instance):
        if not instance.owners.filter(id=self.request.user.id).exists():
            return Response({"message": "Table owner only"}, 403)
        instance.delete()


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsOwner])
def swith_guest_GM(request):
    table = Table.objects.get(id=request.data.get('table_id'))
    user = User.objects.get(id=request.data.get('user_id'))
    message = ""
    if user in table.game_masters.all():
        table.game_masters.remove(user)
        table.guests.add(user)
        message = f"user { user.username } switched to guest"
    elif user in table.guests.all():
        table.guests.remove(user)
        table.game_masters.add(user)
        message = f"user { user.username } switched to game master"
    else:
        raise ValidationError("Impossible to perform this action.")
    serializer = TableSerializer(table)
    return Response({"message": message, "table": serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsOwner])
def switch_GM_owner(request):
    table = Table.objects.get(id=request.data.get('table_id'))
    user = User.objects.get(id=request.data.get('user_id'))
    message = ""
    if user in table.owners.all() and table.owners.count() > 1:
        table.owners.remove(user)
        table.game_masters.add(user)
        message = f"user { user.username } switched to game master"
    elif user in table.game_masters.all():
        table.game_masters.remove(user)
        table.owners.add(user)
        message = f"user { user.username } switched to owner"
    else:
        raise ValidationError("Impossible to perform this action.")
    serializer = TableSerializer(table)
    return Response({"message": message, "table": serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsOwner])
def switch_guest_owner(request):
    table = Table.objects.get(id=request.data.get('table_id'))
    user = User.objects.get(id=request.data.get('user_id'))
    message = ""
    if user in table.owners.all() and table.owners.count() > 1:
        table.owners.remove(user)
        table.guests.add(user)
        message = f"user { user.username } switched to guest"
    elif user in table.guests.all():
        table.guests.remove(user)
        table.owners.add(user)
        message = f"user { user.username } switched to owner"
    else:
        raise ValidationError("Impossible to perform this action.")
    serializer = TableSerializer(table)
    return Response({"message": message, "table": serializer.data})


class CampainViewSet(viewsets.ViewSet):
    """Handle actions on campains"""

    @transaction.atomic
    def create(self, request):
        if not request.user.is_subscriber:
            return Response({"message": "Subscriber only"}, 403)
        message = (
            "Invalid form, be sure the title, the "
            "description, and the charater names do not exceed "
            "31 characters each."
        )
        campain = Campain(
            title=request.data['title'],
            game=request.data['game'],
            image_url=request.data['image_url'],
            language=request.data['language'],
            table=Table.objects.get(id=request.data['table_id']),
            description=request.data['description'],
            game_master=request.user,
            )
        try:
            campain.full_clean()
        except Exception:
            return Response({"errors": [message]}, status=400)
        campain.save()
        return Response({"message": "Campain created"})

    def destroy(self, request, pk=None):
        if not request.user.is_subscriber:
            return Response({"message": "Subscriber only"}, 403)
        campain = Campain.objects.get(id=pk)
        campain.delete()
        return Response({"message": "Campain deleted"})

    def retrieve(self, request, pk=None):
        campain = Campain.objects.get(id=pk)
        campain_serializer = CampainItemsSerializer(campain, context={'request': request})
        datas = {
            'campain': campain_serializer.data,
            'collection': None,
            }
        if campain.parent_collection:
            collection = campain.parent_collection
            collection_serializer = CollectionsSerializer(collection, context={'request': request})
            datas['collection'] = collection_serializer.data

        return Response(datas)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_campain(request):
    """At least a campain id must be provided in the request data"""
    try:
        id = request.data['campain_id']
        campain = Campain.objects.get(id=id)
    except Campain.DoesNotExist:
        raise ValidationError("This campain does not exists")
    if not is_game_master(request.user, campain):
        return Response({"message": "Game master only"}, status=400)
    if 'title' in request.data:
        if request.data['title'] == "":
            return Response({"message": "You must choose a title"}, status=400)
        else:
            campain.title = request.data['title']
    if 'game' in request.data:
        if request.data['game'] == "":
            return Response({"message": "You must choose a game"}, status=400)
        else:
            campain.game = request.data['game']
    if 'language' in request.data:
        if request.data['language'] not in map(lambda x: x[0], LANGUAGES):
            return Response({"message": "Invalid language"}, status=400)
        else:
            campain.language = request.data['language']
    if 'is_ended' in request.data:
        campain.is_ended = request.data['is_ended']
    if 'description' in request.data:
        campain.description = request.data['description']
    if 'image_url' in request.data:
        campain.image_url = request.data['image_url']
    if 'is_copy_free' in request.data and campain.is_copy_free:
        campain.is_copy_free = request.data['is_copy_free']

    campain.save()
    context = {'request': request}
    serializer = CampainSerializer(campain, context=context)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsOwner])
def get_campains_for_table(request):
    table = Table.objects.get(id=request.GET.get('table_id'))
    campains = table.table_campains.all()
    serializer = CampainSerializer(campains, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    # if request.data['title'] == "":
    #     return Response({"message": "You must choose a title"}, status=400)
    if request.data['campainId'] == "":
        return Response({"message": "You must choose a campain"}, status=400)
    if request.data['type'] == "":
        return Response({"message": "You must choose a type"}, status=400)
    locked = True
    date_unlocked = None

    if request.data['type'] == "MEMO":
        locked = False
        date_unlocked = datetime.now()

    if request.user.is_subscriber:
        item_type = request.data['type']
    else:
        item_type = "MEMO"

    item = Item(
        name=request.data['title'],
        campain=Campain.objects.get(id=request.data['campainId']),
        image_url=request.data['image_url'],
        type=item_type,
        data_pc=request.data['pcsInfos'],
        data_gm=request.data['gmInfos'],
        locked=locked,
        date_unlocked=date_unlocked,
        )
    item.save()
    return Response({"message": "ok"})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_item(request):
    """
    Expects an id and the fields to update.
    Updates the item, returns this item's datas.
    """

    try:
        item = Item.objects.get(id=request.data['id'])
        campain = Campain.objects.get(id=item.campain.id)
    except Item.DoesNotExist or campain.DoesNotExist:
        return Response({"message": "Ressource does not exist"}, status=400)
    # only the game master can update a not 'MEMO' item, or a locked item.
    if not is_game_master(request.user, campain) and item.locked:
        return Response({"message": "Game Master only !"}, status=403)
    if not is_game_master(request.user, campain) and item.type != 'MEMO':
        return Response({"message": "Game Master only !"}, status=403)

    if 'name' in request.data:
        item.name = request.data['name']
    if 'image_url' in request.data:
        item.image_url = request.data['image_url']
    if 'type' in request.data:
        item.type = request.data['type']
    if 'data_pc' in request.data:
        item.data_pc = request.data['data_pc']
    if 'data_gm' in request.data:
        if is_game_master(request.user, campain):
            item.data_gm = request.data['data_gm']
    if 'locked' in request.data:
        item.locked = request.data['locked']
        if item.locked:
            item.date_unlocked = None
        else:
            item.date_unlocked = datetime.now()
    item.save()
    serializer = ItemsSerializer(item)

    if not is_game_master(request.user, campain):
        serializer = ItemsPCSerializer(item)

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request):
    """
    Expects an id.
    Deletes the item, returns a message.
    """
    try:
        item = Item.objects.get(id=request.data['id'])
        campain = Campain.objects.get(id=item.campain.id)
    except Item.DoesNotExist or campain.DoesNotExist:
        return Response({"message": "Ressource does not exist"}, status=400)
    # only the game master can delete a not 'MEMO' item
    if item.type != 'MEMO' or item.locked:
        user = request.user
        game_master = campain.game_master
        if user != game_master:
            return Response({"message": "Game Master only !"}, status=403)
    item.delete()
    return Response({"message": "ok"})


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSubscriber])
def create_pc(request):
    """
    Expects a campain id and a name.
    Creates a pc, returns this pc's datas.
    """
    if request.data['campain_id'] == "":
        return Response({"message": "You must choose a campain"}, status=400)
    if request.data['player_id'] != "":
        if User.objects.filter(id=request.data['player_id']).exists():
            user = User.objects.get(id=request.data['player_id'])
        else:
            user = None
    pc = PlayerCharacter(
        name=request.data['name'],
        campain=Campain.objects.get(id=request.data['campain_id']),
        image_url=request.data['image_url'],
        data_pc=request.data['data_pc'],
        data_player=request.data['data_player'],
        data_gm=request.data['data_gm'],
        user=user,
        )
    pc.save()
    serializer = PlayerCharacterSerializer(pc)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_pc(request):
    """
    Expects an id and the fields to update.
    Updates the pc, returns this pc's datas.
    """
    try:
        pc = PlayerCharacter.objects.get(id=request.data['id'])
        campain = Campain.objects.get(id=pc.campain.id)
    except PlayerCharacter.DoesNotExist or campain.DoesNotExist:
        return Response({"message": "Ressource does not exist"}, status=400)
    # only the game master can update a pc
    if not is_game_master(request.user, campain) and not is_player(request.user, pc):
        return Response({"message": "Game Master or player only !"}, status=403)

    if is_player(request.user, pc) or is_game_master(request.user, campain):
        if 'name' in request.data:
            pc.name = request.data['name']
        if 'image_url' in request.data:
            pc.image_url = request.data['image_url']
        if 'data_pc' in request.data:
            pc.data_pc = request.data['data_pc']
        if 'data_player' in request.data:
            pc.data_player = request.data['data_player']
        if is_game_master(request.user, campain):
            if 'data_gm' in request.data:
                pc.data_gm = request.data['data_gm']
            if 'player_id' in request.data:
                if User.objects.filter(id=request.data['player_id']).exists():
                    pc.user = User.objects.get(id=request.data['player_id'])
                else:
                    pc.user = None
            if 'locked' in request.data:
                pc.locked = request.data['locked']
    pc.save()
    serializer = PlayerCharacterSerializer(pc)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_pc(request):
    try:
        campain_id = request.data['campain_id']
        campain = Campain.objects.get(id=campain_id)
        pc = PlayerCharacter.objects.get(id=request.data['id'])
    except PlayerCharacter.DoesNotExist or Campain.DoesNotExist:
        return Response({"message": "Ressource does not exist"}, status=400)
    if pc.campain.id != campain.id:
        return Response({"message": "Ressource does not exist"}, status=400)
    if not is_game_master(request.user, campain):
        return Response({"message": "Game Master only !"}, status=403)
    pc.delete()
    return Response({"message": "ok"})
