# Generated by Django 3.2.4 on 2021-06-21 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20210621_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(blank=True, default=1624274148.8475008),
        ),
        migrations.AlterField(
            model_name='article',
            name='updated_at',
            field=models.TextField(blank=True, default=1624274148.8475125, null=True),
        ),
    ]
