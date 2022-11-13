from api.models import IngredientAmount


def create_ingredient_amount_relations(ingredients, recipe):
    for ingredient in ingredients:
        IngredientAmount.objects.create(
            ingredient_id=ingredient['id'],
            amount=ingredient['amount'],
            recipe=recipe
        )


def get_exists_models_relations(user, model, params):
    if user.is_anonymous:
        return False
    return model.objects.filter(**params).exists()
