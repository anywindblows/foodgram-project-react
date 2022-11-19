import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from api.v1.models import Ingredient

DATA_ROOT = os.path.join(settings.BASE_DIR, '../data/ingredients.json')


class Command(BaseCommand):
    """Basecommand using for uploading ingredients using JSON file."""
    help = 'Loading ingredients from data in json'

    def handle(self, *args, **options):
        try:
            with open(DATA_ROOT, encoding='utf-8') as f:
                data = json.load(f)
                for ingredient in data:
                    try:
                        Ingredient.objects.get_or_create(
                            name=ingredient.get('name'),
                            measurement_unit=ingredient.get('measurement_unit')
                        )
                    except IntegrityError:
                        print(
                            f'Ingredient {ingredient["name"]} '
                            f'{ingredient["measurement_unit"]} '
                            f'already exist in database.'
                        )
        except FileNotFoundError:
            raise CommandError('File does`t exist.')
