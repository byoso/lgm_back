from django.db.models import Q
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Collection, CollectionItem, CollectionPC


class CollectionsSerializer(ModelSerializer):
    """Minimal serializer"""
    author = SerializerMethodField()
    rating = SerializerMethodField()
    votes_count = SerializerMethodField()

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = [
            'id', 'date_created', 'date_updated', 'history', 'author']

    def get_author(self, obj):
        return obj.author.username

    def get_rating(self, obj):
        return obj.rating.average()

    def get_votes_count(self, obj):
        return obj.rating.votes_count



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
    rating = SerializerMethodField()
    votes_count = SerializerMethodField()

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = [
            'id', 'date_created', 'date_updated', 'history', 'author',]

    def get_author(self, obj):
        return obj.author.username

    def get_rating(self, obj):
        return obj.rating.average()

    def get_votes_count(self, obj):
        return obj.rating.votes_count
