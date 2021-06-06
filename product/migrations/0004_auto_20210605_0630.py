# Generated by Django 3.2.4 on 2021-06-05 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210605_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category_detail',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article', to='product.categorydetail'),
        ),
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(default=1622874602.8176775),
        ),
    ]
