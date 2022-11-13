from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from services.api_services import (create_ingredient_amount_relations,
                                   get_exists_models_relations)

from .models import Ingredient, IngredientAmount, Recipe, Tag, Favorite

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for UserModel."""
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )


class TagSerializer(serializers.ModelSerializer):
    """Serializer for TagModel."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for IngredientModel."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Serializer for IngredientAmountModel."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount',)
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientAmount.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):       # TODO: add docstring
    """Serializer for RecipeModel."""
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientAmountSerializer(
        source='ingredientamount_set',
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:                                                     # TODO: NestedValidationError and ValidationError
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        data['ingredients'] = ingredients
        data['tags'] = tags                                         # TODO: VALIDATE ALL (TAGS, INGREDIENTS AND ETC)
        return data

    def create(self, validated_data):
        tags, ingredients = (
            validated_data.pop('tags'),
            validated_data.pop('ingredients')
        )
        recipe = Recipe.objects.create(**validated_data)

        create_ingredient_amount_relations(ingredients, recipe)
        recipe.tags.set(tags)

        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.image)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )

        instance.tags.clear()
        tags = self.initial_data.get('tags')
        instance.tags.set(tags)

        IngredientAmount.objects.filter(recipe=instance).all().delete()

        create_ingredient_amount_relations(
            validated_data.get('ingredients'),
            instance
        )
        instance.save()

        return instance

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        params = {'favorites__user': user, 'id': obj.id}

        return get_exists_models_relations(user, Recipe, params)

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        params = {'cart__user': user, 'id': obj.id}

        return get_exists_models_relations(user, Recipe, params)


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
