# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-09 16:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0015_auto_20171207_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='characteristic',
            field=models.CharField(choices=[('0', '名'), ('1', '代'), ('2', '副'), ('3', '形1'), ('4', '形2'), ('5', '动1'), ('6', '动2'), ('7', '动3'), ('8', '专'), ('9', '叹'), ('10', 'phrase')], max_length=1, verbose_name='词性'),
        ),
        migrations.AlterField(
            model_name='word',
            name='kanji',
            field=models.CharField(blank=True, max_length=30, verbose_name='汉字'),
        ),
    ]