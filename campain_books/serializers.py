from django.db.models import Q
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from django.contrib.auth import get_user_model

from django_silly_auth.serializers import UserInfosSerializer

from .models import Table, Campain, PlayerCharacter, Item, Collection
from .helpers import is_game_master, is_player
from .serializers_collections import CollectionsSerializer

User = get_user_model()


class TableMiniSerializer(ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'name']

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
    name = serializers.CharField(required=True, max_length=31)

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
    pcs = PlayerCharacterSerializer(read_only=True, many=True)
    table = TableSerializer(read_only=True)
    game_master = UserInfosSerializer(read_only=True)
    title = serializers.CharField(required=True, max_length=31)
    description = serializers.CharField(required=False, max_length=31)
    parent_collection = SerializerMethodField()

    class Meta:
        model = Campain
        fields = (
            'id',
            'title',
            'pcs',
            'table',
            'game',
            'game_master',
            'description',
            'is_ended',
            'image_url',
            'language',
            'is_official',
            'official_url',
            'is_copy_free',
            'parent_collection',
            )
        read_only_fields = [
            'id', 'date_created', 'date_updated',
            'is_official', 'official_url',
            'parent_collection',
            ]

    def get_parent_collection(self, obj):
        print('obj in serializer :', obj.parent_collection)
        parent_collection = obj.parent_collection
        serializer = CollectionsSerializer(
            parent_collection,
            context={'request': self.context['request']},
            )
        return serializer.data


class CampainItemsSerializer(ModelSerializer):
    """Campain including items with all datas"""
    items = ItemsSerializer(read_only=True, many=True)
    pcs = SerializerMethodField()
    table = TableSerializer(read_only=True)
    game_master = UserInfosSerializer(read_only=True)
    title = serializers.CharField(required=True, max_length=31)
    description = serializers.CharField(required=False, max_length=31)

    class Meta:
        model = Campain
        fields = (
            'id',
            'title',
            'pcs',
            'table',
            'game',
            'game_master',
            'description',
            'is_ended',
            'items',
            'image_url',
            'language',
            'is_official',
            'official_url',
            'is_copy_free',
            )
        read_only_fields = [
            'id', 'date_created', 'date_updated',
            'is_official',
            'official_url',
            ]

    def get_pcs(self, obj):
        try:
            user = self.context['request'].user
        except KeyError:
            pcs = PlayerCharacter.objects.filter(campain=obj)
        if is_game_master(user, obj):
            pcs = PlayerCharacter.objects.filter(campain=obj)
        else:
            pcs = PlayerCharacter.objects.filter(campain=obj, locked=False)
        return PlayerCharacterSerializer(pcs, many=True).data
