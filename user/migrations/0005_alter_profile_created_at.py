# Generated by Django 3.2.4 on 2021-06-11 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_profile_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='created_at',
            field=models.TextField(default=1623409565.421571),
        ),
    ]
