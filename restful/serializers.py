# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers

from dictionaries import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class DictionarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Dictionary
        fields = ('url', 'name', 'created_at', 'updated_at')


class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Chapter
        fields = ('url', 'name', 'created_at', 'updated_at')
