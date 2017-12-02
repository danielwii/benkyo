from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api import serializers
from dictionaries import models


@api_view(['GET'])
def api_root(request):
    return Response({
        'dictionaries': reverse('api:dictionary-list', request=request),
    })


class DictionaryListView(generics.ListAPIView):
    queryset = models.Dictionary.objects.all()
    serializer_class = serializers.DictionaryListSerializer


class DictionaryDetailView(generics.RetrieveAPIView):
    queryset = models.Dictionary.objects.filter()
    serializer_class = serializers.DictionaryDetailSerializer


class ChapterDetailView(generics.RetrieveAPIView):
    queryset = models.Chapter.objects.filter()
    serializer_class = serializers.ChapterDetailSerializer
