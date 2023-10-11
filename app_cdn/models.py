import uuid
from django.db import models
from django.core.exceptions import ValidationError

CATEGORIES = (
    ('js', 'JavaScript'),
    ('json', 'JSON'),
    ('css', 'CSS'),
    ('html', 'HTML'),
    ('img', 'Image'),
    ('doc', 'Document'),
    ('other', 'Other'),
)


class Project(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


def item_directory(instance, filename):
    return f'{instance.project.name}/{instance.category}/{filename}'


class Item(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='items')
    category = models.CharField(max_length=10, choices=CATEGORIES, default='other')
    name = models.CharField(max_length=150, null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to=item_directory)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'description', '-date']

    def __str__(self):
        return f'{self.name} - {self.category}'
