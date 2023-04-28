from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Table

from django_silly_auth.serializers import UserInfosSerializer

User = get_user_model()


class TableSerializer(ModelSerializer):
    owners = UserInfosSerializer(read_only=True, many=True)
    class Meta:
        model = Table
        fields = '__all__'


class DashboardSerializer(serializers.Serializer):

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    # tables_as_owner = serializers.PrimaryKeyRelatedField(
    #     queryset=Table.objects.all(),
    #     many=True,
    #     read_only=True,
    # )
    # tables_as_user = serializers.PrimaryKeyRelatedField(
    #     queryset=Table.objects.all(),
    #     many=True,
    #     read_only=True,
    # )
