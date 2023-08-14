import uuid

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class HomeArticle(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, default="", blank=True)
    content = models.TextField(default="", blank=True)  # accepts markdown
    show = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    image_url = models.URLField(default="", blank=True)
    image_size = models.IntegerField(
        default=100,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )

    def __str__(self):
        return self.title
