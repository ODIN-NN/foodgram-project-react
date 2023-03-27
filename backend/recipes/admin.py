from django.contrib import admin

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'color',
    )
    search_fields = (
        'name', 'slug'
    )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author', 'name', 'cooking_time', 'get_favorites', 'get_ingredients',
    )
    search_fields = ('name', 'author', 'tags')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    def get_favorites(self, obj):
        return obj.favorites.count()
    get_favorites.short_description = 'Избранные рецепты'

    def get_ingredients(self, obj):
        return ', '.join([
            ingredients.name for ingredients
            in obj.ingredients.all()])
    get_ingredients.short_description = 'Ингредиенты'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('user', )
    empty_value_display = '-пусто-'


admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
