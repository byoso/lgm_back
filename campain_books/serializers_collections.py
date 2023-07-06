from django.db.models import Q
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Collection, CollectionItem, CollectionPC


class CollectionsSerializer(ModelSerializer):
    author = SerializerMethodField()

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = [
            'id', 'date_created', 'date_updated', 'history', 'author']

    def get_author(self, obj):
        return obj.author.username


class CollectionItemSerializer(ModelSerializer):
    class Meta:
        model = CollectionItem
        fields = '__all__'
        read_only_fields = [
            'id',
        ]


class CollectionPCSerializer(ModelSerializer):
    class Meta:
        model = CollectionPC
        fields = '__all__'
        read_only_fields = [
            'id',
        ]


class CollectionsFullSerializer(ModelSerializer):
    """Used in the exchanges views to display the full collection"""
    author = SerializerMethodField()
    pcs = CollectionPCSerializer(many=True, read_only=True)
    items = CollectionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = [
            'id', 'date_created', 'date_updated', 'history', 'author']

    def get_author(self, obj):
        return obj.author.username
