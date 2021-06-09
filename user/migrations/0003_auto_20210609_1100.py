# Generated by Django 3.2.4 on 2021-06-09 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210609_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='user.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.TextField(default=1623236437.9968195),
        ),
    ]
