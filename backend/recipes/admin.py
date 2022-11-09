from django.contrib import admin

from .models import Ingredient, MeasurementUnit, Tag


class TagModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color', 'slug']
    list_filter = ['name', 'slug']


class IngredientModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'measurement_unit']
    list_filter = ['name', 'measurement_unit']


class MeasurementUnitModelAdmin(admin.ModelAdmin):
    list_display = ['unit']
    list_filter = ['unit']


admin.site.register(Tag, TagModelAdmin)
admin.site.register(Ingredient, IngredientModelAdmin)
admin.site.register(MeasurementUnit, MeasurementUnitModelAdmin)
