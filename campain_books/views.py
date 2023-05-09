import uuid

from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets


from .models import Table
from .serializers import TableSerializer
from .permissions import IsOwner, IsGuestOrOwner
from .helpers import guests_create_or_not

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tables_as_owner(request):
    tables = Table.objects.filter(owners=request.user)
    serializer = TableSerializer(tables, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tables_as_user(request):
    tables = Table.objects.filter(users=request.user)
    serializer = TableSerializer(tables, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    data = dict()
    tables_as_owner = Table.objects.filter(owners=request.user)
    serializer = TableSerializer(tables_as_owner, many=True)
    tables_as_guest = Table.objects.filter(guests=request.user)
    serializer2 = TableSerializer(tables_as_guest, many=True)

    data["tables_as_owner"] = serializer.data
    data["tables_as_guest"] = serializer2.data

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_table_datas(request):
    id = request.GET.get('table_id')
    print("====== ID: ", id)
    if Table.objects.filter(id=request.GET.get('table_id')).exists():
        table = Table.objects.get(id=request.GET.get('table_id'))
        serializer = TableSerializer(table)
        return Response(serializer.data)
    raise ValidationError("This table does not exists")


class TableViewSet(viewsets.ModelViewSet):
    """Handle actions on tables but"""
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated, IsGuestOrOwner]

    def get_queryset(self):
        user = self.request.user
        return Table.objects.filter(owners=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            table = serializer.save()
            table.owners.add(self.request.user)

            response_datas = guests_create_or_not(
                self.request,
                guests_list=self.request.data.get('guests'),
                table=table, message="",
                serializer=serializer,
                )
            return Response(response_datas)
        raise ValidationError(serializer.errors)

    def perform_update(self, serializer):
        if serializer.is_valid():
            table = serializer.save()

            response_datas = guests_create_or_not(
                self.request,
                guests_list=self.request.data.get('guests'),
                table=table, message="",
                serializer=serializer,
                )
            return Response(response_datas)
        raise ValidationError(serializer.errors)

    def perform_destroy(self, instance):
        instance.delete()
