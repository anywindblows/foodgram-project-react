import io
from typing import Any, Dict, List, Type, Union

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import serializers, status
from rest_framework.response import Response

from api.v1.models import Cart, Favorite, Ingredient, IngredientRecipe, Recipe
from config import config_messages as msg


def create_ingredient_amount_relations(
        ingredients: List[Dict[str, str]], recipe: Recipe
) -> None:
    """Create relations between recipe and ingredientsamount models."""
    for ingredient in ingredients:
        IngredientRecipe.objects.create(
            ingredient_id=ingredient['id'],
            amount=ingredient['amount'],
            recipe=recipe
        )


def get_exists_models_relations(
        user: Any, model: Type[Recipe], params: Dict[str, Any]
) -> bool:
    """Return boolean value of the filtered model."""
    return (
        False if user.is_anonymous
        else model.objects.filter(**params).exists()
    )


def create_obj(
        model: Type[Union[Favorite, Cart]], serializer, user: Any, pk: int
) -> Response:
    """Adding recipe to favorite list or return error (400)."""
    if model.objects.filter(user=user, recipe__id=pk).exists():
        return Response(
            {'errors': msg.RECIPE_ALREADY_EXIST},
            status=status.HTTP_400_BAD_REQUEST
        )
    recipe = get_object_or_404(Recipe, id=pk)
    model.objects.create(user=user, recipe=recipe)
    serializer = serializer(recipe)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_obj(
        model: Type[Union[Favorite, Cart]], user: Any, pk: int
) -> Response:
    """Remove recipe from favorite list or return error (400)."""
    obj = model.objects.filter(user=user, recipe__id=pk)
    if obj.exists():
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(
        {'errors': f'{msg.CANT_FIND_RECIPE}: {pk}.'},
        status=status.HTTP_400_BAD_REQUEST
    )


def validate_value(value, model=None, field_name=None) -> Type[
    Union[Recipe, Ingredient, None]
]:
    """Validate value and check is decimal."""
    if not str(value).isdecimal():
        raise serializers.ValidationError(f'{value} {msg.SHOULD_BE_INTEGER}')
    if model:
        obj = model.objects.filter(id=value)
        if not obj:
            raise serializers.ValidationError(
                {field_name: f'{value} {msg.NOT_EXIST}'}
            )
        return obj[0]
    return None


def check_data_to_list_isinstance(ingredients: list, tags: list) -> None:
    """Check data to type (list) and is not None."""
    for value in (ingredients, tags):
        if not isinstance(value, list):
            raise serializers.ValidationError(
                f'"{value}" {msg.SHOULD_BE_LIST}.'
            )


def check_data_is_not_none(ingredients: list, tags: list) -> None:
    """Check data is not None."""
    if not ingredients:
        raise serializers.ValidationError(
            {'ingredients': msg.MIN_ONE_INGREDIENT}
        )
    if not tags:
        raise serializers.ValidationError(
            {'tags': msg.MIN_ONE_TAG}
        )


def check_ingredients_is_unique(ingredients):
    """Check ingredients and raise error if is not unique."""
    if len(ingredients) > len({x['id']: x for x in ingredients}.values()):
        raise serializers.ValidationError(msg.UNIQUE_INGREDIENTS)


def create_buy_list(ingredients: QuerySet) -> Dict[str, dict]:
    """Create buy list with unique ingredients for all recipes in cart."""
    buy_list = dict()
    for ingredient in ingredients:
        if ingredient[0] not in buy_list:
            buy_list[ingredient[0]] = {
                'measurement_unit': ingredient[1],
                'amount': ingredient[2]
            }
        else:
            buy_list[ingredient[0]]['amount'] += ingredient[2]
    return buy_list


def create_pdf_file(data: Dict[str, dict]) -> io.BytesIO:
    """Create pdf file with buy list."""
    height = 770
    width = 75
    buffer = io.BytesIO()
    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf', 'UTF-8'))
    p = canvas.Canvas(buffer)
    p.setFont('DejaVuSerif', size=14)
    p.drawString(75, 800, f'{msg.INGR_LIST}:')
    p.setFont('DejaVuSerif', size=12)
    for i, (name, data) in enumerate(data.items(), 1):
        p.drawString(
            x=width,
            y=height,
            text=f'{i}) {name} - {data["amount"]}, {data["measurement_unit"]}'
        )
        height -= 15
    p.showPage()
    p.save()
    buffer.seek(0)

    return buffer
