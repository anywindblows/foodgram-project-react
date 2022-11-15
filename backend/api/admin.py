from django.contrib import admin

from .models import Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag


class TagModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color', 'slug']
    list_filter = ['name', 'slug']


class IngredientModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'measurement_unit']
    list_filter = ['name', 'measurement_unit']


class RecipeModelAdmin(admin.ModelAdmin):
    list_display = ['author', 'name', 'image', 'text', 'cooking_time']
    list_filter = ['author', 'name', 'ingredients', 'tags', 'cooking_time']


class IngredientAmountModelAdmin(admin.ModelAdmin):
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
admin.site.register(IngredientAmount, IngredientAmountModelAdmin)
