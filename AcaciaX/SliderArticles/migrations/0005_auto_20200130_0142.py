# Generated by Django 2.2 on 2020-01-30 01:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SliderArticles', '0004_auto_20200130_0122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment2',
            name='article_comment2',
        ),
        migrations.RemoveField(
            model_name='comment2',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='comment2',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Comment2',
        ),
    ]