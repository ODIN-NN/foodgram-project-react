from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Рецептурные тэги."""
    name = models.CharField(
        verbose_name='Тэг',
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Тэг-слаг',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name', )

    def __str__(self):
        return f'{self.name} {self.color}'

    def clean(self):
        self.name = self.name.strip().lower()
        self.slug = self.slug.strip().lower()
        return super().clean()


class Ingredient(models.Model):
    """Ингредиенты."""
    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=200,
        db_index=True,
        unique=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=24
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ('name', )

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'

    def clean(self):
        self.name = self.name.lower()
        self.measurement_unit = self.measurement_unit.lower()
        super().clean()


class Recipe(models.Model):
    """Рецепты."""
    name = models.CharField(
        verbose_name='Блюдо',
        max_length=200,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipes',
        through='recipes.QuantityIngredient',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг',
        related_name='recipes',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        editable=False,
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipes/image/',
    )
    text = models.TextField(
        verbose_name='Описание',
        max_length=5000
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(MinValueValidator
                    (1, message='Не менее 1 мин'),
                    MaxValueValidator
                    (1440, message='Слишком долго, закажите пиццу)))')),
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='unique_recipe_for_one_author'
            ),
        ]

    def __str__(self):
        return f'{self.name}. Автор: {self.author.username}'

    def clean(self):
        self.name = self.name.capitalize()
        return super().clean()


class QuantityIngredient(models.Model):
    """Вспомогательная модель, связывающая модели Recipe и Ingredient."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты',
        related_name='ingredient',
        on_delete=models.CASCADE,
    )
    ingredients = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиенты в рецепте',
        related_name='recipe',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=0,
        validators=(
            MinValueValidator(1, message='Слишком мало'),
            MaxValueValidator(50, message='Слишком много'),
        ),
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Количество ингридиентов'
        ordering = ('recipe',)
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredients',),
                name='unique_ingredient_in_one_recipe',
            ),
        ]

    def __str__(self) -> str:
        return (f'{self.quantity} '
                f'{self.ingredients.measurement_unit} {self.ingredients}')


class FavoriteRecipes(models.Model):
    """Избранные рецепты."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Избранные рецепты',
        related_name='favorite',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favorite_recipes',
        on_delete=models.CASCADE,
    )
    date_add = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        default_related_name = 'favorites'
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user',),
                name='recipe_in_favorite',
            ),
        ]

    def __str__(self):
        return f'{self.user}  {self.recipe}'


class Cart(models.Model):
    """Корзина"""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты в корзине',
        related_name='in_cart',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name='Покупатель',
        related_name='cart',
        to=User,
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        default_related_name = 'shopping_list'
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user', ),
                name='recipe_in_cart',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.user} {self.recipe}'
