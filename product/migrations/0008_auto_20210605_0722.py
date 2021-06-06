# Generated by Django 3.2.4 on 2021-06-05 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filter', '0001_initial'),
        ('product', '0007_auto_20210605_0720'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='category_detail',
        ),
        migrations.AddField(
            model_name='article',
            name='category_detail',
            field=models.ManyToManyField(related_name='article', to='filter.CategoryDetail'),
        ),
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(default=1622877764.7330015),
        ),
    ]
