# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 10:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0008_auto_20171204_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selectedword',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionaries.Profile', verbose_name='所属'),
        ),
    ]