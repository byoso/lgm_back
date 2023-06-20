# Generated by Django 4.2 on 2023-06-19 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campain_books', '0022_collection_history'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ('date_updated',)},
        ),
        migrations.AddField(
            model_name='collection',
            name='image_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]