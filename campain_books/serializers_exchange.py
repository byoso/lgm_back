
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
    # is_copy_free = SerializerMethodField()

    class Meta:
        model = Campain
        fields = ['id', 'title', 'is_copy_free', 'game']
        read_only_fields = ['id', 'title', 'is_copy_free', 'game']

    # def get_is_copy_free(self, obj):
    #     user = self.context['request'].user
    #     if obj.parent_collection:
    #         if obj.parent_collection.author == user:
    #             return True
    #         return obj.parent_collection.is_copy_free
    #     return True


class CollectionExchangesMiniSerializer(ModelSerializer):
    # is_copy_free = SerializerMethodField()

    class Meta:
        model = Collection
        fields = ['id', 'title', 'is_copy_free', 'game']
        read_only_fields = ['id', 'title', 'is_copy_free', 'game']

    # def get_is_copy_free(self, obj):
    #     user = self.context['request'].user
    #     if obj.author == user:
    #         return True
    #     return False
