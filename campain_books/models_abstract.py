import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()

LANGUAGES = [

    ('ar', _('Arabic')),
    ('cs', _('Czech')),
    ('zh', _('Chinese')),
    ('da', _('Danish')),
    ('nl', _('Dutch')),
    ('en', _('English')),
    ('fi', _('Finnish')),
    ('fr', _('French')),
    ('de', _('German')),
    ('el', _('Greek')),
    ('hi', _('Hindi')),
    ('hu', _('Hungarian')),
    ('it', _('Italian')),
    ('ja', _('Japanese')),
    ('ko', _('Korean')),
    ('no', _('Norwegian')),
    ('fa', _('Persian')),
    ('pl', _('Polish')),
    ('pt', _('Portuguese')),
    ('ru', _('Russian')),
    ('es', _('Spanish')),
    ('sv', _('Swedish')),
    ('th', _('Thai')),
    ('tr', _('Turkish')),
    ('vi', _('Vietnamese')),
]


class AbstractItem(models.Model):
    TYPE_CHOICES = (
        ('NPC', _('Non-Player Character')),
        ('LOCATION', _('Location')),
        ('ORGANIZATION', _('Organization')),
        ('EVENT', _('Event')),
        ('NOTE', _('Note')),
        ('RECAP', _('Recap')),
        ('MISC', _('Misc')),
        ('MEMO', _('Memo')),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=31, default='')
    image_url = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='MEMO')
    data_pc = models.TextField(default='')
    data_gm = models.TextField(default='')  # always locked for PCs

    class Meta:
        ordering = ('type', 'name',)
        abstract = True

    def __str__(self):
        return f"<Item: {self.name}>"


class AbstractPC(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=63, null=True, blank=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    data_pc = models.TextField(blank=True, null=True)
    data_player = models.TextField(blank=True, null=True)
    data_gm = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    locked = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return f"<PlayerCharacter: {self.name} - {self.id}>"


class AbstractCampain(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(max_length=63, default='', blank=True)
    language = models.CharField(choices=LANGUAGES, max_length=2, default='en')
    image_url = models.CharField(max_length=255, blank=True, null=True)
    game = models.CharField(max_length=63, default='', blank=True)
    description = models.TextField(
        blank=True, null=True,
        validators=[MaxLengthValidator(63)]
        )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"<AbstractCampain: {self.name} - {self.id}>"
