# Generated by Django 4.2 on 2023-08-14 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_homearticle_subtitle_alter_homearticle_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homearticle',
            name='image_url',
            field=models.URLField(default=''),
        ),
    ]
