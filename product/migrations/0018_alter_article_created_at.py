# Generated by Django 3.2.4 on 2021-06-13 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_alter_article_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(default=1623562502.2824612),
        ),
    ]
