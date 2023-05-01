import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _


class Table(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=63)
    owners = models.ManyToManyField(
        to=get_user_model(),
        related_name='tables_owned',
        blank=True,
    )
    description = models.TextField(blank=True, null=True)
    guests = models.ManyToManyField(
        to="Guest",
        related_name='tables',
        blank=True,
        )
    table_password = models.CharField(max_length=63, blank=True, null=True)
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
        ('notif', _('Notification')),
        ('note', _('Note')),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=63, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=63, blank=True, null=True)
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
        max_length=63,
        blank=True, null=True,
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(63),
        ]
    )
    description = models.TextField(blank=True, null=True)
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
    game_masters = models.ManyToManyField(to=get_user_model(), related_name='campains_gm')
    ended = models.BooleanField(default=False)

    def __str__(self):
        return f"<Campain: {self.name}>"


class PlayerCharacter(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='pcs')
    character_name = models.CharField(max_length=63)
    campain = models.ForeignKey(to=Campain, on_delete=models.CASCADE, related_name='pcs')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"<PlayerCharacter: {self.name}>"


class CampainTemplate(AbstractCampain):
    GAMES = (
        ('misc', _('Miscellaneous')),
        ('DnD', _('Dungeons & Dragons')),
        ('LGM', _('Le Grand Monde')),
        ('SWd6', _('Star Wars d6')),
        ('SWd20', _('Star Wars d20')),
        ('NOC', _('NOC')),
        ('DH', _('Dark Heresy')),
        ('WH', _('Warhammer')),
        ('INS/MV', _('In Nomine Satanis/Magna Veritas')),
        ('Cthulhu', _('Call of Cthulhu')),
        ('Vampire', _('Vampire')),
        ('critical', _('Critical')),
    )
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
    author = models.ForeignKey(to=get_user_model(), on_delete=models.DO_NOTHING, related_name='books')
    game = models.CharField(max_length=63, choices=GAMES)
    rating = models.IntegerField(blank=True, null=True, choices=RATINGS)
    played_times = models.IntegerField(default=0)
    master = models.OneToOneField(to='Campain', on_delete=models.DO_NOTHING, related_name='template')

    def __str__(self):
        return f"<CampainTemplate: {self.name}>"


class Guest(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(max_length=63, unique=True)
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name='guest',
        blank=True, null=True)

    def __str__(self):
        return f"<Guest: {self.name}>"

    @property
    def is_valid_user(self):
        if self.user is not None and self.user.is_active and \
                self.user.is_confirmed:
            return True
        return False
