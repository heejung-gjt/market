# Generated by Django 3.2.8 on 2021-10-25 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20211025_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(blank=True, default=1635120345.321621),
        ),
        migrations.AlterField(
            model_name='article',
            name='updated_at',
            field=models.TextField(blank=True, default=1635120345.3216348, null=True),
        ),
    ]
