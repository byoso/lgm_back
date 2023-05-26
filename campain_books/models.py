import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Game(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=31)
    description = models.TextField(max_length=255, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    official_site = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Game')
        verbose_name_plural = _('Games')
        ordering = ['name']

    def __str__(self):
        return f"<Game: {self.name}>"

    def perform_create(self, serializer):
        serializer.save(owners=self.request.user)


class Table(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=31)
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
    table_password = models.CharField(max_length=31, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Table: {self.name}>"

    def perform_create(self, serializer):
        serializer.save(owners=self.request.user)


class Item(models.Model):
    TYPE_CHOICES = (
        ('npc', _('Non-Player Character')),
        ('place', _('Place')),
        ('orga', _('Organisation')),
        ('event', _('Event')),
        ('note', _('Note')),
        ('recap', _('Recap')),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=31, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=31, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    campain = models.ForeignKey(to='Campain', on_delete=models.CASCADE, related_name='items')
    type = models.CharField(max_length=31, choices=TYPE_CHOICES)
    locked = models.BooleanField(default=True)
    data_pc = models.TextField(blank=True, null=True)
    data_gm = models.TextField(blank=True, null=True) # always locked for PCs

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"<Item: {self.name}>"


class AbstractCampain(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(
        max_length=31,
        blank=True, null=True,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(31),
        ]
    )
    description = models.TextField(
        blank=True, null=True,
        validators=[MaxLengthValidator(31)]
        )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"<AbstractCampain: {self.name}>"


class Campain(AbstractCampain):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    game_master = models.ForeignKey(
        to="PlayerCharacter",
        related_name='campain_gm',
        on_delete=models.CASCADE,
        blank=True, null=True,
        )
    is_ended = models.BooleanField(default=False)
    game = models.ForeignKey(
        Game, on_delete=models.PROTECT,
        related_name='game_campains',
        blank=True, null=True)

    table = models.ForeignKey(
        Table, on_delete=models.CASCADE,
        related_name='table_campains',
        )

    def __str__(self):
        return f"<Campain: {self.title}>"


class CampainTemplate(AbstractCampain):
    RATINGS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    author = models.ForeignKey(to=get_user_model(), on_delete=models.PROTECT, related_name='books')
    rating = models.IntegerField(blank=True, null=True, choices=RATINGS)
    played_times = models.IntegerField(default=0)
    master = models.OneToOneField(to='Campain', on_delete=models.PROTECT, related_name='template')
    game = models.ForeignKey(
        Game, on_delete=models.PROTECT,
        related_name='campains',
        blank=True, null=True)

    def __str__(self):
        return f"<CampainTemplate: {self.name}>"


class PlayerCharacter(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='campain_users'
        )
    character_name = models.CharField(max_length=31, null=True, blank=True)
    campain = models.ForeignKey(
        to=Campain,
        related_name='campain_pcs',
        on_delete=models.CASCADE,
        blank=True, null=True,
        )
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"<PlayerCharacter: {self.character_name}>"
