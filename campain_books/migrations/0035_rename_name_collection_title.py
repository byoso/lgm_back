# Generated by Django 4.2 on 2023-07-03 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campain_books', '0034_remove_campain_is_collectible'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection',
            old_name='name',
            new_name='title',
        ),
    ]
