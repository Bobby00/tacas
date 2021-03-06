# Generated by Django 2.2 on 2020-01-30 10:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0010_comment2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preference',
            name='value',
            field=models.IntegerField(choices=[(1, 'like'), (-1, 'dislike')]),
        ),
        migrations.AlterUniqueTogether(
            name='preference',
            unique_together={('user', 'post')},
        ),
    ]
