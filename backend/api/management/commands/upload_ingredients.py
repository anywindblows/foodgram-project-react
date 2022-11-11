import os
import json

from django.conf import settings
from api.models import Ingredient
from django.core.management.base import BaseCommand, CommandError

DATA_ROOT = os.path.join(settings.BASE_DIR, '../data/ingredients.json')
print(settings.BASE_DIR)


class Command(BaseCommand):
    help = 'loading ingredients from data in json'

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
