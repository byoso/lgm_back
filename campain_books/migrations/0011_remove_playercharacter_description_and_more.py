# Generated by Django 4.2 on 2023-06-05 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campain_books', '0010_alter_campain_language_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playercharacter',
            name='description',
        ),
        migrations.AddField(
            model_name='playercharacter',
            name='data_public',
            field=models.TextField(blank=True, null=True),
        ),
    ]