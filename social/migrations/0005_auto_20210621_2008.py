# Generated by Django 3.2.4 on 2021-06-21 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_auto_20210621_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TextField(blank=True, default=1624273684.8556964),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated_at',
            field=models.TextField(blank=True, default=1624273684.8557131, null=True),
        ),
    ]
