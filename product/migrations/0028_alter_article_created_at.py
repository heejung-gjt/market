# Generated by Django 3.2.4 on 2021-06-16 09:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_auto_20210616_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 6, 16, 9, 51, 25, 356054)),
        ),
    ]
