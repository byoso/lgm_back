# Generated by Django 4.2 on 2023-06-14 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campain_books', '0020_alter_collectionitem_collection_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='game',
            field=models.CharField(blank=True, max_length=63, null=True),
        ),
    ]
