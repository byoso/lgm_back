# Generated by Django 4.2 on 2023-07-07 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campain_books', '0039_alter_campain_title_alter_collection_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campain',
            options={'ordering': ('table', 'title')},
        ),
        migrations.AlterModelOptions(
            name='collectionitem',
            options={'ordering': ('type', 'name')},
        ),
        migrations.AlterModelOptions(
            name='collectionpc',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('type', 'name')},
        ),
        migrations.AlterModelOptions(
            name='playercharacter',
            options={'ordering': ('locked', '-user', 'name')},
        ),
        migrations.RemoveField(
            model_name='collection',
            name='rating',
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('votes_count', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
                ('collection', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='campain_books.collection')),
                ('voters', models.ManyToManyField(related_name='ratings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
