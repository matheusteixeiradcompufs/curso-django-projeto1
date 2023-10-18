from django.urls import reverse, resolve

from recipes import views
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
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here :(</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_recipes = response.context['recipes']

        self.assertIn('Titulo da Receita', content)
        self.assertEqual(len(response_recipes), 1)

    def test_recipe_home_template_load_recipes_not_published(self):
        self.make_recipe(recipe_is_published=False)

        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            '<h1>No recipes found here :(</h1>',
            response.content.decode('utf-8')
        )

    # tests to category views
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1, }))
        self.assertTrue(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_category_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1, }))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a cotegory test'
        self.make_recipe(recipe_title=needed_title)

        response = self.client.get(reverse('recipes:category', args=(1, )))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_category_template_load_recipes_not_published(self):
        recipe = self.make_recipe(recipe_is_published=False)

        response = self.client.get(reverse('recipes:category', args=(recipe.category.id, )))

        self.assertEqual(response.status_code, 404)

    # tests to recipe views
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'recipe_id': 1, }))
        self.assertTrue(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'recipe_id': 1, }))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It load one recipe'
        self.make_recipe(recipe_title=needed_title)

        response = self.client.get(reverse('recipes:recipe', args=(1, )))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_detail_template_load_recipes_not_published(self):
        recipe = self.make_recipe(recipe_is_published=False)

        response = self.client.get(reverse('recipes:recipe', args=(recipe.id, )))

        self.assertEqual(response.status_code, 404)
