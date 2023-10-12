from django.shortcuts import render, get_object_or_404, get_list_or_404

from recipes.models import Recipe
from utils.recipes.factory import make_recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(category=category_id, is_published=True).order_by('-id')
    )
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - Category | '
    })


def recipe(request, recipe_id):
    recipe_content = get_object_or_404(Recipe, id=recipe_id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe_content,
        'is_detail_page': True
    })
