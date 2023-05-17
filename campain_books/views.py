import uuid

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets

from .models import Table, Game, Campain, PlayerCharacter
from .serializers import TableSerializer, GameSerializer, PlayerCharacterSerializer, CampainSerializer
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

    def create(self, request):
        pcs = request.data['pcs']
        campain = Campain.objects.create(
            title=request.data['title'],
            game=Game.objects.get(id=request.data['game_id']),
            table=Table.objects.get(id=request.data['table_id']),
            description=request.data['description'],
            )
        for pc in pcs.values():
            if not User.objects.filter(id=pc['id']).exists():
                raise ValidationError(f"User {pc['id']} does not exists")
            user = User.objects.get(id=pc['id'])
            if pc['name'] == "":
                pc_name = user.username
            else:
                pc_name = pc['name']

            new_pc = PlayerCharacter.objects.create(
                character_name=pc_name, user=user, )
            new_pc.campains.add(campain)
            new_pc.save()
            if str(new_pc.user.id) == request.data['master_id']:
                campain.game_master = new_pc
                campain.save()
        return Response({"message": "ok"})


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsOwner])
def get_campains_for_table(request):
    table = Table.objects.get(id=request.GET.get('table_id'))
    campains = table.table_campains.all()
    serializer = CampainSerializer(campains, many=True)
    return Response(serializer.data)
