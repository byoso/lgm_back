# Generated by Django 4.2 on 2023-06-01 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campain_books', '0006_item_date_unlocked_alter_item_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='author',
        ),
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(choices=[('NPC', 'Non-Player Character'), ('LOCATION', 'Location'), ('ORGANISATION', 'Organisation'), ('EVENT', 'Event'), ('NOTE', 'Note'), ('RECAP', 'Recap'), ('MISC', 'Misc'), ('MEMO', 'Memo')], max_length=31),
        ),
    ]
