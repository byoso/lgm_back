from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Table

from django_silly_auth.serializers import UserInfosSerializer

User = get_user_model()


class TableSerializer(ModelSerializer):
    # TODO: (or not) maybe change the serializer for a more specific one
    owners = UserInfosSerializer(read_only=True, many=True)
    guests = UserInfosSerializer(read_only=True, many=True)

    class Meta:
        model = Table
        fields = [
            'id',
            'name',
            'description',
            'table_password',
            'owners',
            'guests',
        ]
