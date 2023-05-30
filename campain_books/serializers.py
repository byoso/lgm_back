from django.db.models import Q
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Table, Game, Campain, PlayerCharacter, Item

from django_silly_auth.serializers import UserInfosSerializer

User = get_user_model()


class TableSerializer(ModelSerializer):
    owners = UserInfosSerializer(read_only=True, many=True)
    guests = UserInfosSerializer(read_only=True, many=True)

    class Meta:
        model = Table
        fields = [
            'id',
            'name',
            'description',
            'owners',
            'guests',
        ]


class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ['id', 'date_created', 'date_updated']


class PlayerCharacterSerializer(ModelSerializer):
    user = UserInfosSerializer(read_only=True)
    character_name = serializers.CharField(required=True, max_length=31)

    class Meta:
        model = PlayerCharacter
        fields = '__all__'
        read_only_fields = ['id', 'date_created', 'date_updated']

class CampainIdSerializer(ModelSerializer):
    class Meta:
        model = Campain
        fields = ['id']
        read_only_fields = ['id']

class GetPCItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['id', 'date_created', 'date_updated']


class GetGMItemSerializer(ModelSerializer):
    campain = CampainIdSerializer(read_only=True)
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['id', 'date_created', 'date_updated', 'campain']


class CampainSerializer(ModelSerializer):
    items = GetGMItemSerializer(read_only=True, many=True)
    campain_pcs = PlayerCharacterSerializer(read_only=True, many=True)
    table = TableSerializer(read_only=True)
    game = GameSerializer(read_only=False)
    game_master = PlayerCharacterSerializer(read_only=False)
    title = serializers.CharField(required=True, max_length=31)
    description = serializers.CharField(required=False, max_length=31)

    class Meta:
        model = Campain
        fields = (
            'id',
            'title',
            'campain_pcs',
            'table',
            'game',
            'game_master',
            'description',
            'is_ended',
            'items',
            )
        read_only_fields = ['id', 'date_created', 'date_updated']
