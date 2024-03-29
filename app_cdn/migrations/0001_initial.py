# Generated by Django 4.2.4 on 2023-08-21 23:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('github', models.URLField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('js', 'JavaScript'), ('css', 'CSS'), ('html', 'HTML'), ('img', 'Image'), ('doc', 'Document'), ('other', 'Other')], default='other', max_length=10)),
                ('name', models.CharField(max_length=150)),
                ('file', models.FileField(blank=True, null=True, upload_to='uploads/')),
                ('url', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='app_cdn.project')),
            ],
            options={
                'ordering': ['category', '-date'],
            },
        ),
    ]
