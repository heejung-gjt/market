# Generated by Django 3.2.6 on 2021-09-07 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20210907_2246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_liked',
        ),
        migrations.AddField(
            model_name='user',
            name='is_address',
            field=models.BooleanField(default=False, verbose_name='Is address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.TextField(blank=True, default=1631024094.722936),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.TextField(blank=True, default=1631024094.7229483, null=True),
        ),
    ]