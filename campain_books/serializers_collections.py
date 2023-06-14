from django.db.models import Q
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Collection


class CollectionsSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ['id', 'date_created', 'date_updated', 'history']
