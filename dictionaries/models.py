# -*- coding: utf-8 -*-
from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ('created_at',)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Dictionary(BaseModel):
    class Meta:
        verbose_name_plural = 'dictionaries'
        ordering = ('created_at',)

    name = models.CharField(max_length=10, verbose_name='名称')

    def __str__(self):
        return self.name


class Chapter(BaseModel):
    class Meta:
        ordering = ('created_at',)

    name = models.CharField(max_length=10, verbose_name='章节')

    dictionary = models.ForeignKey(Dictionary, related_name='chapters', on_delete=models.CASCADE, verbose_name='所属字典')

    def __str__(self):
        return "%s - %s" % (self.dictionary, self.name)


CHARACTERISTIC_CHOICES = (
    ('0', '名词'),
)


class Word(BaseModel):
    class Meta:
        ordering = ('created_at',)

    kana = models.CharField(max_length=30, verbose_name='假名')
    kanji = models.CharField(max_length=30, verbose_name='汉字')
    marking = models.CharField(max_length=100, blank=True, verbose_name='假名标注')
    characteristic = models.CharField(
        max_length=1,
        choices=CHARACTERISTIC_CHOICES,
        verbose_name='词性'
    )
    meaning = models.TextField(verbose_name='意思')
    # tone 音调
    # characteristic 词性

    chapter = models.ForeignKey(Chapter, verbose_name='所属章节')

    def __str__(self):
        return self.kanji
