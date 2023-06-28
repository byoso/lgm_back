import uuid

from django.db import models
from django.contrib.auth import get_user_model

from .models_abstract import (
    AbstractItem,
    AbstractPC,
    AbstractCampain,
    LANGUAGES,
    RATINGS,
    )

User = get_user_model()


class Table(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=63)
    owners = models.ManyToManyField(
        to=User,
        related_name='tables_owned',
        blank=True,
    )
    description = models.TextField(blank=True, null=True)
    guests = models.ManyToManyField(
        to=User,
        related_name='tables',
        blank=True,
        )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Table: {self.name} - {self.id}>"

    def perform_create(self, serializer):
        serializer.save(owners=self.request.user)


class Item(AbstractItem):
    campain = models.ForeignKey(
        to='Campain', on_delete=models.CASCADE, related_name='items'
        )
    locked = models.BooleanField(default=True)
    date_unlocked = models.DateTimeField(blank=True, null=True)


class PlayerCharacter(AbstractPC):
    campain = models.ForeignKey(
        to="Campain",
        related_name='campain_pcs',
        on_delete=models.CASCADE,
        )
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        related_name='campain_users',
        blank=True, null=True,
        )

    class Meta:
        ordering = ('locked', '-user', '-name')


class Campain(AbstractCampain):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    game_master = models.ForeignKey(
        to=User,
        related_name='campain_gm',
        on_delete=models.CASCADE,
        blank=True, null=True,
        )
    is_ended = models.BooleanField(default=False)

    parent_collection = models.ForeignKey(
        to="Collection",
        on_delete=models.SET_NULL,
        related_name='children_campains',
        blank=True, null=True,
        )
    # is_collectible = models.BooleanField(default=True)
    is_official = models.BooleanField(default=False)
    official_url = models.CharField(max_length=255, blank=True, null=True)

    table = models.ForeignKey(
        Table, on_delete=models.CASCADE,
        related_name='table_campains',
        )

    def __str__(self):
        return f"<Campain: {self.title} - {self.id}>"


class CollectionItem(AbstractItem):
    collection = models.ForeignKey(
        to="Collection",
        on_delete=models.CASCADE,
        related_name='items',
        )

    def __str__(self):
        return f"<CollectionItem: {self.name} - {self.id}>"

    class Meta:
        ordering = ('type', '-date_created')


class CollectionPC(AbstractPC):
    collection = models.ForeignKey(
        to="Collection",
        on_delete=models.CASCADE,
        related_name='pcs',
        )

    def __str__(self):
        return f"<CollectionPC: {self.name} - {self.id}>"


class Collection(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=63)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='collections'
        )
    game = models.CharField(max_length=63, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(choices=LANGUAGES, max_length=2, default='en')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    rating = models.IntegerField(blank=True, null=True, choices=RATINGS)
    times_played = models.IntegerField(default=0)
    is_official = models.BooleanField(default=False)
    official_url = models.CharField(max_length=255, blank=True, null=True)
    is_shared = models.BooleanField(default=False)
    history = models.TextField(blank=True, null=True)
    # if copyright, prevents cloning.
    is_copy_free = models.BooleanField(default=False)

    #  items and pcs are related_name

    class Meta:
        ordering = ('-is_official', 'rating', '-date_updated', 'game')

    def __str__(self):
        return f"<Collection: {self.name} - {self.id}>"
