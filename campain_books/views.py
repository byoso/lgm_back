from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


from .models import Table
from .serializers import TableSerializer, DashboardSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_table(request):
    serializer = TableSerializer(
                    data=request.data,
                    )
    if serializer.is_valid():
        table = serializer.save()
        table.owners.add(request.user)
        return Response(serializer.data)
    raise ValidationError(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    serializer = DashboardSerializer(
        data=request.data,
        context={'request': request
                 })
    if serializer.is_valid():
        return Response(serializer.data)
    raise ValidationError(serializer.errors)


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
def show_table(request):
    data = [dict()]
    tables = Table.objects.filter(owners=request.user)
    serializer = TableSerializer(tables, many=True)
    data[0]["tables_as_owner"] = serializer.data

    data[0]["additionnal_data"] = "some data"
    # data.append({"additionnal_data": "some data"})
    return Response(data)
