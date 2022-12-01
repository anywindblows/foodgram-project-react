from typing import Dict, List, Union

from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from services.api_services import (check_data_is_not_none,
                                   check_data_to_list_isinstance,
                                   check_ingredients_is_unique,
                                   create_ingredient_amount_relations,
                                   get_exists_models_relations,
                                   validate_value)
from users.models import Follow

from .models import Ingredient, IngredientRecipe, Recipe, Tag

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


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Serializer for IngredientRecipeModel."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientRecipe.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for RecipeModel."""
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipeSerializer(
        source='ingredientrecipe_set',
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def validate(self, data):
        """Validate data before create new relations."""
        ingredients, tags = (
            self.initial_data.get('ingredients'),
            self.initial_data.get('tags')
        )

        check_data_to_list_isinstance(ingredients, tags)
        check_data_is_not_none(ingredients, tags)
        check_ingredients_is_unique(ingredients)

        for tag in tags:
            validate_value(tag, Tag, 'Tag')

        validated_ing = list()

        for ing in ingredients:
            ing_id, amount = ing.get('id'), ing.get('amount')
            ingredient = validate_value(ing_id, Ingredient, 'Ingredient')

            validate_value(amount)
            validated_ing.append({'ingredient': ingredient, 'amount': amount})

        data['ingredients'], data['tags'] = ingredients, tags
        return data

    def create(self, validated_data: Dict[str, Union[List, str]]) -> Recipe:
        """Create new recipe."""
        tags, ingredients = (
            validated_data.pop('tags'),
            validated_data.pop('ingredients')
        )
        recipe = Recipe.objects.create(**validated_data)

        create_ingredient_amount_relations(ingredients, recipe)
        recipe.tags.set(tags)

        return recipe

    def update(
            self,
            instance: Recipe,
            validated_data: Dict[str, Union[str, List[Dict[str, str]]]]
    ) -> Recipe:
        """Update recipe."""
        instance.name = validated_data.get('name', instance.image)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )

        instance.tags.clear()
        tags = self.initial_data.get('tags')
        instance.tags.set(tags)

        IngredientRecipe.objects.filter(recipe=instance).all().delete()

        create_ingredient_amount_relations(
            validated_data.get('ingredients'),
            instance
        )
        instance.save()

        return instance

    def get_is_favorited(self, obj: Recipe) -> bool:
        """Return favorite recipes for user."""
        user = self.context.get('request').user
        params = {'favorites__user': user, 'id': obj.id}

        return get_exists_models_relations(user, Recipe, params)

    def get_is_in_shopping_cart(self, obj: Recipe) -> bool:
        """Return recipes added to cart."""
        user = self.context.get('request').user
        params = {'cart__user': user, 'id': obj.id}

        return get_exists_models_relations(user, Recipe, params)


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Short recipe representation."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for FollowModel."""
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    @staticmethod
    def get_is_subscribed(obj):
        """Return boolean value of subscribed status."""
        return Follow.objects.filter(user=obj.user, author=obj.author).exists()

    @staticmethod
    def get_recipes_count(obj):
        """Return integer value for the number of recipes."""
        return Recipe.objects.filter(author=obj.author).count()

    def get_recipes(self, obj):
        """
        Return recipes set.
        If @param 'recipes_limit' in request
        returns a set given a slice by constraint.
        """
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        return ShortRecipeSerializer(queryset, many=True).data
