# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0006_auto_20171201_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='characteristic',
            field=models.CharField(choices=[(0, b'\xe5\x90\x8d\xe8\xaf\x8d')], default='', max_length=1, verbose_name=b'\xe8\xaf\x8d\xe6\x80\xa7'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='word',
            name='marking',
            field=models.CharField(blank=True, max_length=100, verbose_name=b'\xe5\x81\x87\xe5\x90\x8d\xe6\xa0\x87\xe6\xb3\xa8'),
        ),
    ]
