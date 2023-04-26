from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Table
from .serializers import TableSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_table(request):
    serializer = TableSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)
