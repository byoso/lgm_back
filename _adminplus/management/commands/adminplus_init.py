import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from _adminplus.models import Configuration

User = get_user_model()


class Command(BaseCommand):
    """Django command to pause initialize the adminplus configuration singleton"""

    def handle(self, *args, **options):
        print('Adminplus initialization...')
        try:
            # the try/except is here to avoid a migration error
            if not Configuration.objects.filter(id__gte=1).exists():
                Configuration.objects.create()
                print('Adminplus Configuration created')
            else:
                print('Adminplus Configuration already exists')
        except Exception as e:
            print('Adminplus initialization error: \n')
            print(e)
