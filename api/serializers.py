# -*- coding: utf-8 -*-
from rest_framework import serializers

from dictionaries import models


class DictionaryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dictionary
        fields = ('url', 'id', 'name', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    url = serializers.HyperlinkedIdentityField(view_name='api:dictionary-detail')


class DictionaryChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chapter
        fields = ('url', 'id', 'name', 'created_at', 'updated_at')

    url = serializers.HyperlinkedIdentityField(view_name='api:chapter-detail')


class DictionaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dictionary
        fields = ('id', 'name', 'chapters', 'created_at', 'updated_at')

    chapters = DictionaryChapterSerializer(many=True, read_only=True)


class ChapterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chapter
        fields = ('id', 'name', 'created_at', 'updated_at')
