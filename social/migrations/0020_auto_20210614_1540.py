# Generated by Django 3.2.4 on 2021-06-14 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0019_auto_20210614_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='is_checked',
        ),
        migrations.RemoveField(
            model_name='recomment',
            name='is_checked',
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TextField(default=1623685241.3647757),
        ),
        migrations.AlterField(
            model_name='recomment',
            name='created_at',
            field=models.TextField(default=1623685241.3647757),
        ),
    ]