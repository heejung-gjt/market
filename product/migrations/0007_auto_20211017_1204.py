# Generated by Django 3.2.8 on 2021-10-17 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20211017_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(blank=True, default=1634439847.893507),
        ),
        migrations.AlterField(
            model_name='article',
            name='updated_at',
            field=models.TextField(blank=True, default=1634439847.8935187, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.TextField(verbose_name='product image'),
        ),
    ]