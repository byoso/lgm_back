from datetime import datetime

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

from .models import Table, Game, Campain, PlayerCharacter, Item
from .serializers import (
    TableSerializer, GameSerializer,
    PlayerCharacterSerializer, CampainSerializer,
    GetGMItemSerializer, GetPCItemSerializer,
    )
from .permissions import IsOwner, IsGuestOrOwner
from .helpers import guests_create_or_not

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

    data["tables_as_owner"] = serializer.data
    data["tables_as_guest"] = serializer2.data

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
        instance.delete()


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsOwner])
def switch_guest_owner(request):
    print("=== table id: ", request.data.get('table_id'))
    print(request.POST)
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_games_list(request):
    serializer = GameSerializer(Game.objects.all(), many=True)
    return Response(serializer.data)


class CampainViewSet(viewsets.ViewSet):
    """Handle actions on campains"""

    @transaction.atomic
    def create(self, request):
        message = (
            "Invalid form, be sure the title, the "
            "description, and the charater names do not exceed "
            "31 characters each."
        )
        pcs = request.data['pcs']
        campain = Campain(
            title=request.data['title'],
            game=Game.objects.get(id=request.data['game_id']),
            table=Table.objects.get(id=request.data['table_id']),
            description=request.data['description'],
            )
        try:
            campain.full_clean()
        except Exception:
            return Response({"errors": [message]}, status=400)
        campain.save()
        for pc in pcs.values():
            if not User.objects.filter(id=pc['id']).exists():
                raise ValidationError(f"User {pc['id']} does not exists")
            user = User.objects.get(id=pc['id'])
            if pc['name'] == "":
                pc_name = "< anonymous PC >"
            else:
                pc_name = pc['name']

            new_pc = PlayerCharacter(
                character_name=pc_name, user=user, )
            try:
                new_pc.full_clean()
            except Exception:
                return Response({"errors": [message]}, status=400)
            new_pc.campain = campain
            new_pc.save()
            if str(new_pc.user.id) == request.data['master_id']:
                campain.game_master = new_pc
                campain.save()
        if not campain.game_master:
            return Response(
                {"errors": ["You must choose a game master"]},
                status=400
                )
        return Response({"message": "ok"})

    def destroy(self, request, pk=None):
        campain = Campain.objects.get(id=pk)
        campain.delete()
        return Response({"message": "ok"})

    def retrieve(self, request, pk=None):
        campain = Campain.objects.get(id=pk)
        serializer = CampainSerializer(campain)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsOwner])
def get_campains_for_table(request):
    table = Table.objects.get(id=request.GET.get('table_id'))
    campains = table.table_campains.all()
    serializer = CampainSerializer(campains, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    if request.data['title'] == "":
        return Response({"message": "You must choose a title"}, status=400)
    if request.data['campainId'] == "":
        return Response({"message": "You must choose a campain"}, status=400)
    if request.data['type'] == "":
        return Response({"message": "You must choose a type"}, status=400)
    locked = True
    date_unlocked = None
    if request.data['type'] == "MEMO":
        locked = False
        date_unlocked = datetime.now()
    item = Item(
        author=request.user,
        name=request.data['title'],
        campain=Campain.objects.get(id=request.data['campainId']),
        image_url=request.data['image_url'],
        type=request.data['type'],
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
    # print(request.data)
    try:
        item = Item.objects.get(id=request.data['id'])
        campain = Campain.objects.get(id=item.campain.id)
    except Item.DoesNotExist or campain.DoesNotExist:
        return Response({"message": "Ressource does not exist"}, status=400)
    # only the game master can update a not 'MEMO' item
    if item.type != 'MEMO':
        user = request.user
        game_master = campain.game_master.user
        if user != game_master:
            return Response({"message": "You are not the game master"}, status=403)
    if 'name' in request.data:
        item.name = request.data['name']
    if 'image_url' in request.data:
        item.image_url = request.data['image_url']
    if 'type' in request.data:
        item.type = request.data['type']
    if 'data_pc' in request.data:
        item.data_pc = request.data['data_pc']
    if 'data_gm' in request.data:
        item.data_gm = request.data['data_gm']
    if 'locked' in request.data:
        item.locked = request.data['locked']
        if item.locked:
            item.date_unlocked = None
        else:
            item.date_unlocked = datetime.now()
    item.save()

    serializer = GetGMItemSerializer(item)
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
    if item.type != 'MEMO':
        user = request.user
        game_master = campain.game_master.user
        if user != game_master:
            return Response({"message": "You are not the game master"}, status=403)
    item.delete()
    return Response({"message": "ok"})
