# Generated by Django 3.2.6 on 2021-09-07 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20210907_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.TextField(blank=True, default=1631022378.5651548),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.TextField(blank=True, default=1631022378.5651665, null=True),
        ),
    ]
