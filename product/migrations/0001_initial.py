# Generated by Django 3.2.6 on 2021-08-05 01:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('created_at', models.TextField(blank=True, default=1628126770.079433)),
                ('updated_at', models.TextField(blank=True, default=1628126770.0794566, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('content', models.TextField()),
                ('origin_price', models.IntegerField(null=True)),
                ('price', models.IntegerField(default=0)),
                ('image', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to='filter.category')),
                ('category_detail', models.ManyToManyField(blank=True, related_name='article', to='filter.CategoryDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_rate', models.FloatField(default=0)),
                ('article', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article_price', to='product.article')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='image/')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo', to='product.article')),
            ],
        ),
    ]
