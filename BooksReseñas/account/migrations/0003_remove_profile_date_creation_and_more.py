# Generated by Django 5.0.6 on 2024-06-19 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_date_creation_profile_date_updated_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='date_creation',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='date_updated',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user_updated',
        ),
    ]
