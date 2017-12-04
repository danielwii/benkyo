# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 10:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dictionaries', '0007_auto_20171201_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SelectedWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ranks', models.IntegerField(default=0, verbose_name='熟悉度')),
                ('correct_rate', models.IntegerField(verbose_name='正确率')),
                ('correct_times', models.IntegerField(default=0, verbose_name='正确次数')),
                ('wrong_times', models.IntegerField(default=0, verbose_name='错误次数')),
                ('last_checked_at', models.DateTimeField(verbose_name='最后记忆时间')),
                ('last_wrong_at', models.DateTimeField(verbose_name='最后错误时间')),
                ('review_times', models.IntegerField(default=0, verbose_name='复习次数')),
                ('mem_level', models.IntegerField(default=0, verbose_name='记忆阶段')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='dictionary',
            options={'ordering': ('created_at',), 'verbose_name_plural': 'dictionaries'},
        ),
        migrations.AlterModelOptions(
            name='word',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterField(
            model_name='chapter',
            name='dictionary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='dictionaries.Dictionary', verbose_name='所属字典'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(max_length=10, verbose_name='章节'),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='name',
            field=models.CharField(max_length=10, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='word',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionaries.Chapter', verbose_name='所属章节'),
        ),
        migrations.AlterField(
            model_name='word',
            name='characteristic',
            field=models.CharField(choices=[('0', '名词')], max_length=1, verbose_name='词性'),
        ),
        migrations.AlterField(
            model_name='word',
            name='kana',
            field=models.CharField(max_length=30, verbose_name='假名'),
        ),
        migrations.AlterField(
            model_name='word',
            name='kanji',
            field=models.CharField(max_length=30, verbose_name='汉字'),
        ),
        migrations.AlterField(
            model_name='word',
            name='marking',
            field=models.CharField(blank=True, max_length=100, verbose_name='假名标注'),
        ),
        migrations.AlterField(
            model_name='word',
            name='meaning',
            field=models.TextField(verbose_name='意思'),
        ),
        migrations.AddField(
            model_name='selectedword',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionaries.Word', verbose_name='原词'),
        ),
        migrations.AddField(
            model_name='selectedword',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]
