# Generated by Django 4.2 on 2023-06-06 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campain_books', '0017_rename_character_name_playercharacter_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='playercharacter',
            name='image_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]