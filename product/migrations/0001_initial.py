# Generated by Django 3.2.8 on 2021-10-11 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('created_at', models.TextField(blank=True, default=1633949494.1769378)),
                ('updated_at', models.TextField(blank=True, default=1633949494.1769493, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('content', models.TextField()),
                ('origin_price', models.IntegerField(null=True)),
                ('price', models.IntegerField(default=0)),
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
