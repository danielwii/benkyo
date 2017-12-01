# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response

from dictionaries import models
from . import serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class DictionaryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = models.Dictionary.objects.all()
    serializer_class = serializers.DictionarySerializer


class ChapterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Chapter.objects.all()
    serializer_class = serializers.ChapterSerializer
