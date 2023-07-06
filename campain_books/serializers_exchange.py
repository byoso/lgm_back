
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
    table = SerializerMethodField()

    class Meta:
        model = Campain
        fields = ['id', 'title', 'is_copy_free', 'game', 'table']
        read_only_fields = ['id', 'title', 'is_copy_free', 'game']

        ordering = ['table', 'game', 'title']

    def get_table(self, obj):
        return obj.table.name


class CollectionExchangesMiniSerializer(ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'title', 'is_copy_free', 'game', 'author']
        read_only_fields = ['id', 'title', 'is_copy_free', 'game', 'author']
