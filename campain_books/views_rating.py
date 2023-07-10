from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    Rating,
    Collection,
)
from .serializers_collections import CollectionsSerializer

class Ratings(GenericAPIView):
    permission_classes: [IsAuthenticated, ]

    def put(self, obj):
        user = self.request.user
        collection = Collection.objects.get(id=self.request.data['collection_id'])
        rating = collection.rating
        rating.add_vote(user, self.request.data['rate'])

        serializer = CollectionsSerializer(collection, context={'request': self.request})
        print("===", serializer.data)

        return Response({'collection': serializer.data})
