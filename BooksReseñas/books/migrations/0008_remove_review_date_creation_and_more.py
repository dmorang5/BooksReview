# Generated by Django 5.0.6 on 2024-06-19 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_book_date_creation_book_date_updated_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='date_creation',
        ),
        migrations.RemoveField(
            model_name='review',
            name='date_updated',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user_updated',
        ),
    ]
