# Generated by Django 3.2.6 on 2021-09-07 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20210907_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.TextField(blank=True, default=1631019653.7458332),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.TextField(blank=True, default=1631019653.7458456, null=True),
        ),
    ]