# Generated by Django 2.0 on 2017-12-11 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectedword',
            name='last_review_times_needed',
            field=models.IntegerField(default=0, verbose_name='最后所需 Review 次数'),
        ),
    ]
