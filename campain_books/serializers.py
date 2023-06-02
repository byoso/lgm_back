from django.db.models import Q
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Table, Campain, PlayerCharacter, Item

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


class PlayerCharacterSerializer(ModelSerializer):
    user = UserInfosSerializer(read_only=True)
    character_name = serializers.CharField(required=True, max_length=31)

    class Meta:
        model = PlayerCharacter
        fields = '__all__'
        read_only_fields = ['id', 'date_created', 'date_updated']


class CampainIdSerializer(ModelSerializer):
    """Serializer for the campain id only"""
    class Meta:
        model = Campain
        fields = ['id']
        read_only_fields = ['id']


class ItemsPCSerializer(ModelSerializer):
    campain = CampainIdSerializer(read_only=True)
    class Meta:
        model = Item
        exclude = ['data_gm']
        read_only_fields = ['id', 'date_created', 'date_updated', 'campain']


class ItemsSerializer(ModelSerializer):
    campain = CampainIdSerializer(read_only=True)

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['id', 'date_created', 'date_updated', 'campain']


class CampainSerializer(ModelSerializer):
    campain_pcs = PlayerCharacterSerializer(read_only=True, many=True)
    table = TableSerializer(read_only=True)
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
            'image_url',
            'language',
            )
        read_only_fields = ['id', 'date_created', 'date_updated']


class CampainItemsSerializer(ModelSerializer):
    """Campain including items with all datas"""
    items = ItemsSerializer(read_only=True, many=True)
    campain_pcs = PlayerCharacterSerializer(read_only=True, many=True)
    table = TableSerializer(read_only=True)
    # game = GameSerializer(read_only=False)
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
            'image_url',
            'language',
            )
        read_only_fields = ['id', 'date_created', 'date_updated']


class CampainItemsPCSerializer(ModelSerializer):
    """Campain including items with PCs data only"""
    items = ItemsPCSerializer(read_only=True, many=True)
    campain_pcs = PlayerCharacterSerializer(read_only=True, many=True)
    table = TableSerializer(read_only=True)
    # game = GameSerializer(read_only=False)
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
            'image_url',
            'language',
            )
        read_only_fields = ['id', 'date_created', 'date_updated']
