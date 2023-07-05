
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import (
    Collection,
    CollectionItem,
    CollectionPC,
    Campain,
    Item,
    PlayerCharacter,
    )

class CampainExchangesMiniSerializer(ModelSerializer):

    class Meta:
        model = Campain
        fields = ['id', 'title', 'is_copy_free', 'game']
        read_only_fields = ['id', 'title', 'is_copy_free', 'game']


class CollectionExchangesMiniSerializer(ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'title', 'is_copy_free', 'game', 'author']
        read_only_fields = ['id', 'title', 'is_copy_free', 'game', 'author']
