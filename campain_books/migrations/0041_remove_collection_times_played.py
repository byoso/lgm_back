# Generated by Django 4.2 on 2023-07-07 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campain_books', '0040_alter_campain_options_alter_collectionitem_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='times_played',
        ),
    ]
