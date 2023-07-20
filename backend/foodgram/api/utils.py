from django.db.models import Sum
from recipes.models import RecipeIngredient


def get_shopping_cart(user):
    ingredients = RecipeIngredient.objects.filter(
        recipe__carts__user=user
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(ingredient_amount=Sum('amount'))
    shopping_list = ['Список покупок:\n']
    for ingredient in ingredients:
        name = ingredient['ingredient__name']
        unit = ingredient['ingredient__measurement_unit']
        amount = ingredient['ingredient_amount']
        shopping_list.append(f'\n{name} - {amount}, {unit}')
    return shopping_list
