# Generated by Django 2.2 on 2020-01-30 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SliderArticles', '0003_comment_comment2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='article_post',
            new_name='article_comment',
        ),
        migrations.RenameField(
            model_name='comment2',
            old_name='comment',
            new_name='article_comment2',
        ),
    ]