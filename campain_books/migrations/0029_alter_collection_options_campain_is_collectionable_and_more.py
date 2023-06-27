# Generated by Django 4.2 on 2023-06-26 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campain_books', '0028_collection_official_url_alter_collectionitem_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ('-is_official', '-date_updated')},
        ),
        migrations.AddField(
            model_name='campain',
            name='is_collectionable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='campain',
            name='is_official',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='campain',
            name='official_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]