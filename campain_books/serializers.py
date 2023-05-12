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
    players = PlayerCharacterSerializer(read_only=True, many=True)

    class Meta:
        model = Campain
        fields = '__all__'
        read_only_fields = ['id', 'date_created', 'date_updated']