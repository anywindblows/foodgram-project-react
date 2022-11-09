from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=254,
        verbose_name='Tag'
    )

    color = ColorField(
        verbose_name='Color'
    )

    slug = models.SlugField(
        unique=True,
        max_length=254,
        verbose_name='Slug'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        db_table = 'tags'


class MeasurementUnit(models.Model):
    unit = models.CharField(
        unique=True,
        max_length=50,  # DEFINE MAX LENGTH
        verbose_name='Measurement Unit'
    )

    def __str__(self):
        return f'{self.unit}'

    class Meta:
        verbose_name = 'Measurement Unit'
        verbose_name_plural = 'Measurement Units'
        db_table = 'measurement_units'


class Ingredient(models.Model):
    name = models.CharField(
        unique=True,
        max_length=254,
        verbose_name='Ingredients'
    )

    quantity = models.IntegerField(
        verbose_name='Quantity'
    )

    measurement_unit = models.ForeignKey(
        MeasurementUnit,
        on_delete=models.CASCADE,  # complete after connect front
        verbose_name='Measurement unit'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        db_table = 'ingredient'


# class Recipe(models.Model):
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name='Author'
#     )
#
#     name = models.CharField(
#         unique=True,
#         max_length=200,
#         verbose_name='Recipe'
#     )
#
#     image = models.FileField()
#
#     description = models.CharField()
#
#     ingredients = models.ForeignKey(Ingredient)
#
#     tag = models.ForeignKey(Tag)
#
#     time = models.IntegerField()
#
#     def __str__(self):
#         return f'{self.name}'
#
#     class Meta:
#         verbose_name = 'Recipe'
#         verbose_name_plural = 'Recipes'
#         db_table = 'recipes'
