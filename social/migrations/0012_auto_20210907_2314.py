# Generated by Django 3.2.6 on 2021-09-07 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0011_auto_20210907_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TextField(blank=True, default=1631024094.722936),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated_at',
            field=models.TextField(blank=True, default=1631024094.7229483, null=True),
        ),
        migrations.AlterField(
            model_name='recomment',
            name='created_at',
            field=models.TextField(blank=True, default=1631024094.722936),
        ),
        migrations.AlterField(
            model_name='recomment',
            name='updated_at',
            field=models.TextField(blank=True, default=1631024094.7229483, null=True),
        ),
    ]
