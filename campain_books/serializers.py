from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Table, Guest

from django_silly_auth.serializers import UserInfosSerializer

User = get_user_model()


class GuestSerializer(ModelSerializer):
    user = UserInfosSerializer(read_only=True, many=True)

    class Meta:
        model = Guest
        fields = '__all__'


class TableSerializer(ModelSerializer):
    owners = UserInfosSerializer(read_only=True, many=True)
    guests = GuestSerializer(read_only=True, many=True)

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
