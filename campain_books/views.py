from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from django.contrib.auth import get_user_model

from .models import Table, Guest
from .serializers import TableSerializer

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_table(request):
    serializer = TableSerializer(
                    data=request.data,
                    )
    if serializer.is_valid():
        table = serializer.save()
        table.owners.add(request.user)
        for guest_email in request.data.get('guests'):
            if not Guest.objects.filter(email=guest_email).exists():
                guest = Guest.objects.create(email=guest_email)
                if User.objects.filter(email=guest_email).exists():
                    user = User.objects.get(email=guest_email)
                    guest.user = user
                    guest.save()
            else:
                guest = Guest.objects.get(email=guest_email)
            table.guests.add(guest)
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
def dashboard(request):
    data = dict()
    tables_as_owner = Table.objects.filter(owners=request.user)
    serializer = TableSerializer(tables_as_owner, many=True)
    data["tables_as_owner"] = serializer.data

    data["additionnal_data"] = "some data"
    return Response(data)
