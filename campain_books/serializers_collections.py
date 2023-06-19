from django.db.models import Q
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Collection


class CollectionsSerializer(ModelSerializer):
    author = SerializerMethodField()
    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = [
            'id', 'date_created', 'date_updated', 'history']

    def get_author(self, obj):
        return obj.author.username

class CollectionItemSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__',
        read_only_fields = [
            'id',
        ]

class CollectionPCSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__',
        read_only_fields = [
            'id',
        ]