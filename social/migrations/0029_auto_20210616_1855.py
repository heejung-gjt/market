# Generated by Django 3.2.4 on 2021-06-16 09:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0028_auto_20210616_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 6, 16, 18, 55, 42, 362494)),
        ),
        migrations.AlterField(
            model_name='recomment',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 6, 16, 18, 55, 42, 362494)),
        ),
    ]
