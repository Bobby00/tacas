# Generated by Django 2.2 on 2020-03-05 08:43

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
