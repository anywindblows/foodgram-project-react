from api.v1.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                           Recipe, Tag)
from django.contrib import admin


class TagModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color', 'slug']
    list_filter = ['name', 'slug']
    ordering = ('id',)


class IngredientModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'measurement_unit']
    list_filter = ['measurement_unit']
    ordering = ('id',)


class RecipeModelAdmin(admin.ModelAdmin):
    list_display = ['author', 'name', 'image', 'text', 'cooking_time']
    list_filter = ['author', 'name', 'ingredients', 'tags', 'cooking_time']
    ordering = ('id',)


class IngredientRecipeModelAdmin(admin.ModelAdmin):
    list_display = ['ingredient', 'amount']
    list_filter = ['amount']


class FavoriteModelAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user']
    list_filter = ['recipe', 'user']


class CartModelAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user']
    list_filter = ['recipe', 'user']


admin.site.register(Tag, TagModelAdmin)
admin.site.register(Cart, CartModelAdmin)
admin.site.register(Recipe, RecipeModelAdmin)
admin.site.register(Favorite, FavoriteModelAdmin)
admin.site.register(Ingredient, IngredientModelAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeModelAdmin)
