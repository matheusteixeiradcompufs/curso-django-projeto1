from django.test import TestCase
from django.urls import reverse, resolve

from recipes import views
from recipes.models import Category, Recipe, User


class RecipeViewsTest(TestCase):
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
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here :(</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='User',
            last_name='Name',
            username='username',
            password='123456',
            email='user@user.com',
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title='Titulo da Receita',
            description='Descrição da Receita',
            slug='titulo-da-receita',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Pessoas',
            preparation_steps='Passos da Preparação',
            preparation_steps_is_html=False,
            is_published=True,
        )
        assert 1 == 1

    # tests to category views
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1, }))
        self.assertTrue(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1, }))
        self.assertEqual(response.status_code, 404)

    # tests to recipe views
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'recipe_id': 1, }))
        self.assertTrue(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'recipe_id': 1, }))
        self.assertEqual(response.status_code, 404)
