# Generated by Django 4.2 on 2023-06-28 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campain_books', '0033_collection_is_copy_free'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campain',
            name='is_collectible',
        ),
    ]
