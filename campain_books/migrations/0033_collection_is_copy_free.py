# Generated by Django 4.2 on 2023-06-28 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campain_books', '0032_rename_is_collectionable_campain_is_collectible'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='is_copy_free',
            field=models.BooleanField(default=False),
        ),
    ]
