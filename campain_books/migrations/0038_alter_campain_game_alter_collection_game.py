# Generated by Django 4.2 on 2023-07-04 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campain_books', '0037_campain_is_copy_free_alter_collection_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campain',
            name='game',
            field=models.CharField(blank=True, default='', max_length=63),
        ),
        migrations.AlterField(
            model_name='collection',
            name='game',
            field=models.CharField(blank=True, default='', max_length=63),
        ),
    ]
