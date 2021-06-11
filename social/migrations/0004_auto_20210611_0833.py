# Generated by Django 3.2.4 on 2021-06-11 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_article_created_at'),
        ('social', '0003_alter_comment_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.TextField(default=1623400427.4569845)),
                ('updated_at', models.TextField(blank=True, null=True)),
                ('content', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='like',
            old_name='comment',
            new_name='article',
        ),
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment', to='product.article'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TextField(default=1623400427.4569845),
        ),
        migrations.AddField(
            model_name='comment',
            name='recomment',
            field=models.ManyToManyField(blank=True, related_name='comment', to='social.ReComment'),
        ),
    ]