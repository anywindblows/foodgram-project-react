from django.contrib import admin

from .models import Ingredient, IngredientAmount, Recipe, Tag


class TagModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color', 'slug']
    list_filter = ['name', 'slug']


class IngredientModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'measurement_unit']
    list_filter = ['name', 'measurement_unit']


class RecipeModelAdmin(admin.ModelAdmin):
    list_display = [
        'author', 'name', 'image', 'text', 'cooking_time'
    ]
    list_filter = [
        'author', 'name', 'ingredients', 'tags', 'cooking_time'
    ]


class IngredientAmountModelAdmin(admin.ModelAdmin):
    list_display = ['ingredient', 'amount']
    list_filter = ['amount']


admin.site.register(Tag, TagModelAdmin)  # TODO: SORT REGISTER IN IMPORT ORDER
admin.site.register(Ingredient, IngredientModelAdmin)
admin.site.register(Recipe, RecipeModelAdmin)
admin.site.register(IngredientAmount, IngredientAmountModelAdmin)
