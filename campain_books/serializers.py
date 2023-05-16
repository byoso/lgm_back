from django.db.models import Q
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Table, Game, Campain, PlayerCharacter

from django_silly_auth.serializers import UserInfosSerializer

User = get_user_model()


class TableSerializer(ModelSerializer):
    # TODO: (or not) maybe change the serializer for a more specific one
    owners = UserInfosSerializer(read_only=True, many=True)
    guests = UserInfosSerializer(read_only=True, many=True)

    class Meta:
        model = Table
        fields = [
            'id',
            'name',
            'description',
            'table_password',
            'owners',
            'guests',
        ]


class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ['id', 'date_created', 'date_updated']


class PlayerCharacterSerializer(ModelSerializer):
    class Meta:
        model = PlayerCharacter
        fields = '__all__'
        read_only_fields = ['id', 'date_created', 'date_updated']


class CampainSerializer(ModelSerializer):
    pcs = PlayerCharacterSerializer(read_only=True, many=True)
    table = TableSerializer(read_only=True)
    game = GameSerializer(read_only=False)
    game_master = PlayerCharacterSerializer(read_only=False)

    class Meta:
        model = Campain
        fields = (
            # '__all__',
            'id',
            'title',
            'pcs',
            'table',
            'game',
            'game_master',
            'description',
            'is_ended',
            )
        read_only_fields = ['id', 'date_created', 'date_updated']
        depth = 1
