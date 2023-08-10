from django.shortcuts import render

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import (
    HomeArticle,
)

from .serializers import (
    HomeArticleSerializer,
)


class HomeArticleViews(GenericAPIView):

    def get(self, request):
        articles = HomeArticle.objects.filter(show=True).order_by('-date_created')
        serializer = HomeArticleSerializer(articles, many=True)

        return Response({'articles': serializer.data})
