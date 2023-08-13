from django.db import models
from django.db.utils import OperationalError, IntegrityError


class Configuration(models.Model):
    """Config usable for your app, change it to your liking."""
    # just an example (usefull for me):
    open_subscriptions = models.BooleanField(default=True)

    # Add your settings here

    def __str__(self):
        return 'Configuration (singleton)'

    def save(self, *args, **kwargs):
        """This is a singleton, so we only allow one instance."""
        if self.pk == 1 or not self.pk:
            super().save(*args, **kwargs)
        else:
            raise IntegrityError("There can only be one instance of Configuration")


# Create the singleton if it doesn't exist
try:
    # the try/except is here to avoid a migration error
    if not Configuration.objects.all().exists():
        Configuration.objects.create()
except OperationalError:
    pass
