# Generated by Django 4.2 on 2023-05-01 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campain_books', '0003_remove_guest_tables_remove_table_users_guest_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='table',
            old_name='guest',
            new_name='guests',
        ),
    ]