# Generated by Django 3.2.4 on 2021-06-12 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_auto_20210611_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='is_liked',
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TextField(default=1623492563.7930756),
        ),
        migrations.AlterField(
            model_name='recomment',
            name='created_at',
            field=models.TextField(default=1623492563.7930756),
        ),
    ]