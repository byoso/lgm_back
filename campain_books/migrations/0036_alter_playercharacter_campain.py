# Generated by Django 4.2 on 2023-07-03 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campain_books', '0035_rename_name_collection_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playercharacter',
            name='campain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pcs', to='campain_books.campain'),
        ),
    ]