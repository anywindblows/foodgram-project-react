from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Ingredient, Recipe, Tag, IngredientAmount

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

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['measurement_unit'] = instance.measurement_unit
        return response


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Serializer for IngredientAmountModel."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientAmount.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for RecipeModel."""
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientAmountSerializer(
        read_only=True,
        many=True,
        source='ingredientamount_set'
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        )

    def create(self, validated_data):
        image = validated_data.pop('image')
        recipes = Recipe.objects.create(
            image=image,
            **validated_data
        )
        return recipes
