# Generated by Django 2.2 on 2019-12-21 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20191221_0644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsarticle',
            name='news_category',
        ),
        migrations.DeleteModel(
            name='NewsCategory',
        ),
    ]