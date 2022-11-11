from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

User = get_user_model()


class Tag(models.Model):
    """Stores a single tag entry."""
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
    """Stores a single measurement unit entry."""
    unit = models.CharField(
        unique=True,
        max_length=50,  # TODO: DEFINE MAX LENGTH
        verbose_name='Measurement Unit'
    )

    def __str__(self):
        return f'{self.unit}'

    class Meta:
        verbose_name = 'Measurement Unit'
        verbose_name_plural = 'Measurement Units'
        db_table = 'measurement_units'


class Ingredient(models.Model):
    """
    Stores a single ingredient entry,
    related to :model:`measurement_unit.MeasurementUnit`.
    """
    name = models.CharField(
        unique=True,
        max_length=254,
        verbose_name='Ingredients'
    )

    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Measurement unit'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        db_table = 'ingredient'


class Recipe(models.Model):  # TODO: correct max_length param
    """
    Stores a single recipe entry, related to:
    :model:`author.User`,
    :model:`ingredients.Ingredient`,
    :model:`tags.Tag`.
    """
    author = models.ForeignKey(  # TODO: add docstring EVERYWHERE
        User,
        on_delete=models.CASCADE,
        verbose_name='Author'
    )

    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Recipe'
    )

    image = models.ImageField(
        upload_to='images/recipe_images/',
        verbose_name='Image',
    )

    text = models.CharField(
        max_length=512,
        verbose_name='Description'
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ingredients'
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags'
    )

    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Cooking time',
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-name']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        db_table = 'recipes'


class IngredientAmount(models.Model):
    """
    Stores a single ingredient amount entry,
    related to :model:`measurement_unit.MeasurementUnit`.
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ingredients',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Recipe',
    )

    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Amount',
    )

    def __str__(self):
        return f'{self.amount}'

    class Meta:
        verbose_name = 'Ingredient amount'
        verbose_name_plural = 'Ingredients amount'
        db_table = 'ingredient_amount'


class Favorite(models.Model):
    """
    Stores a single favorite recipe entry,
    related to :model:`user.User` and :model:`recipe.Recipe`.
    """

    recipe = models.ManyToManyField(
        Recipe,
        verbose_name='Recipe',
    )

    user = models.ManyToManyField(
        User,
        verbose_name='User'
    )

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        db_table = 'favorites'
