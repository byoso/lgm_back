# Generated by Django 4.2 on 2023-08-14 20:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_homearticle_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homearticle',
            name='image_size',
            field=models.IntegerField(blank=True, default=100, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]
