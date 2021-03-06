# Generated by Django 2.0 on 2017-12-11 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=10, verbose_name='章节')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=10, verbose_name='名称')),
            ],
            options={
                'verbose_name_plural': 'dictionaries',
                'ordering': ('created_at',),
            },
        ),
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
                ('correct_rate', models.IntegerField(null=True, verbose_name='正确率')),
                ('correct_times', models.IntegerField(default=0, verbose_name='正确次数')),
                ('wrong_times', models.IntegerField(default=0, verbose_name='错误次数')),
                ('review_times', models.IntegerField(default=0, verbose_name='复习次数')),
                ('last_checked_at', models.DateTimeField(null=True, verbose_name='最后记忆时间')),
                ('next_check_point', models.DateTimeField(null=True, verbose_name='下次检查点')),
                ('last_wrong_at', models.DateTimeField(null=True, verbose_name='最后错误时间')),
                ('mem_level', models.IntegerField(default=0, verbose_name='记忆阶段')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kana', models.CharField(max_length=30, verbose_name='假名')),
                ('kanji', models.CharField(blank=True, max_length=30, verbose_name='汉字')),
                ('marking', models.CharField(blank=True, max_length=100, verbose_name='假名标注')),
                ('characteristic', models.CharField(choices=[('0', '名'), ('1', '代'), ('2', '副'), ('3', '形1'), ('4', '形2'), ('5', '动1'), ('6', '动2'), ('7', '动3'), ('8', '专'), ('9', '叹'), ('10', '连'), ('11', '连体'), ('12', '疑'), ('99', 'phrase')], max_length=2, verbose_name='词性')),
                ('meaning', models.TextField(verbose_name='意思')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='dictionaries.Chapter', verbose_name='所属章节')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.AddField(
            model_name='selectedword',
            name='origin',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dictionaries.Word', verbose_name='原词'),
        ),
        migrations.AddField(
            model_name='selectedword',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_words', to='dictionaries.Profile', verbose_name='所属'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='dictionary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='dictionaries.Dictionary', verbose_name='所属字典'),
        ),
    ]
