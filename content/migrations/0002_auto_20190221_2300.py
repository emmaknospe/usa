# Generated by Django 2.1.3 on 2019-02-21 23:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2019, 2, 21, 23, 0, 10, 725097, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='edited',
            field=models.DateTimeField(auto_now=True),
        ),
    ]