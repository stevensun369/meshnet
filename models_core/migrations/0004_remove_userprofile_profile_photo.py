# Generated by Django 3.0.8 on 2020-09-01 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models_core', '0003_userprofile_profile_photo_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_photo',
        ),
    ]
