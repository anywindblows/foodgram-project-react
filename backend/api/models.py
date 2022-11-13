from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Stores a single tag entry."""
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Tag'
    )

    color = ColorField(
        unique=True,
        verbose_name='Color',
        max_length=7
    )

    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name='Slug'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        db_table = 'tags'


class Ingredient(models.Model):
    """
    Stores a single ingredient entry,
    related to :model:`measurement_unit.MeasurementUnit`.
    """
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Ingredients'
    )

    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Measurement unit'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        db_table = 'ingredients'


class Recipe(models.Model):
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
        through='IngredientAmount',
        related_name='recipes',
        verbose_name='Ingredients'
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags'
    )

    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Cooking time',
        validators=[MinValueValidator(limit_value=1)]
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
        validators=[MinValueValidator(limit_value=1)],
        verbose_name='Amount',
    )

    def __str__(self):
        return f'{self.amount}'

    class Meta:
        verbose_name = 'Ingredient amount'
        verbose_name_plural = 'Ingredients amount'
        db_table = 'ingredients_amount'


class Favorite(models.Model):
    """
    Stores a single favorite recipe entry,
    related to :model:`recipe.Recipe` and :model:`user.User`.
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Recipe',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='User',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        db_table = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='Favorite user recipes'
            )
        ]


class Cart(models.Model):
    """
    Stores a single user cart entry,
    related to :model:`recipe.Recipe` and :model:`user.User`.
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Recipe',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='User',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        db_table = 'cart'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='User carts'
            )
        ]
