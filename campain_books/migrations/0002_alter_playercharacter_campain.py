# Generated by Django 4.2 on 2023-05-25 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campain_books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playercharacter',
            name='campain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='campain_pcs', to='campain_books.campain'),
        ),
    ]
