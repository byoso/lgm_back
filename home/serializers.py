from rest_framework import serializers

from .models import HomeArticle


class HomeArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeArticle
        fields = '__all__'
        read_only_fields = ['id', 'date_created', 'date_updated']
