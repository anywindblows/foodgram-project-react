import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from api.models import Ingredient

DATA_ROOT = os.path.join(settings.BASE_DIR, '../data/ingredients.json')
print(settings.BASE_DIR)


class Command(BaseCommand):     # TODO: Switch to --flag filename and use without full path.
    help = 'loading ingredients from data in json'      # TODO: fix errors

    def handle(self, *args, **options):
        try:
            with open(DATA_ROOT, encoding='utf-8') as f:
                data = json.load(f, )
                for ingredient in data:
                    Ingredient.objects.get_or_create(
                        name=ingredient.get('name'),
                        measurement_unit=ingredient.get('measurement_unit')
                    )
        except FileNotFoundError:
            raise CommandError('File does`t exist.')
