import uuid

from django.db import models


class HomeArticle(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    title = models.CharField(max_length=255, default="", blank=True, null=True)
    subtitle = models.CharField(max_length=255, default="", blank=True, null=True)
    content = models.TextField(default="")  # accepts markdown
    show = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
