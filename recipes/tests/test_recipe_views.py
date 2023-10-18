from django.urls import reverse, resolve

from recipes import views
from recipes.models import Category, Recipe, User
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):

    # tests to home views
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertTrue(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        Recipe.objects.get(pk=1).delete()
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here :(</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_recipes = response.context['recipes']

        self.assertIn('Titulo da Receita', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Pessoas', content)
        self.assertEqual(len(response_recipes), 1)

    # tests to category views
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1, }))
        self.assertTrue(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_category_found(self):
        Category.objects.get(pk=1).delete()
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1, }))
        self.assertEqual(response.status_code, 404)

    # tests to recipe views
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'recipe_id': 1, }))
        self.assertTrue(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        Recipe.objects.get(pk=1).delete()
        response = self.client.get(reverse('recipes:recipe', kwargs={'recipe_id': 1, }))
        self.assertEqual(response.status_code, 404)
