# Generated by Django 4.1.7 on 2023-03-29 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_users', '0002_alter_user_email_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='new_email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]