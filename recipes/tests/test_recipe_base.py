import io

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from recipes.models import Category, Recipe, User


def make_image():
    with open("C:\\Users\\matheus.teixeira\\Pictures\\2002261230095343-04.jpg", "rb") as image_file:
        image_bytes = image_file.read()
    # Crie uma imagem temporária em memória
    Image.open(io.BytesIO(image_bytes))
    return SimpleUploadedFile("test_image.jpg", image_bytes, content_type="image/jpeg")


class RecipeMixin:
    def make_category(name_category='Category'):
        return Category.objects.create(name=name_category)

    def make_author(
            author_first_name='User',
            author_last_name='Name',
            author_username='username',
            author_password='123456',
            author_email='username@email.com',
    ):
        return User.objects.create_user(
            first_name=author_first_name,
            last_name=author_last_name,
            username=author_username,
            password=author_password,
            email=author_email,
        )

    def make_recipe(self,
            recipe_category=None,
            recipe_author=None,
            recipe_title='Titulo da Receita',
            recipe_description='Descrição da Receita',
            recipe_slug='titulo-da-receita',
            recipe_preparation_time=10,
            recipe_preparation_time_unit='Minutos',
            recipe_servings=5,
            recipe_servings_unit='Pessoas',
            recipe_preparation_steps='Passos da Preparação',
            recipe_preparation_steps_is_html=False,
            recipe_is_published=True
        ):
        if recipe_category is None:
            recipe_category = {}
        if recipe_author is None:
            recipe_author = {}

        return Recipe.objects.create(
            category=self.make_category(**recipe_category),
            author=self.make_author(**recipe_author),
            title=recipe_title,
            description=recipe_description,
            slug=recipe_slug,
            preparation_time=recipe_preparation_time,
            preparation_time_unit=recipe_preparation_time_unit,
            servings=recipe_servings,
            servings_unit=recipe_servings_unit,
            preparation_steps=recipe_preparation_steps,
            preparation_steps_is_html=recipe_preparation_steps_is_html,
            is_published=recipe_is_published,
            cover=make_image()
        )

    def make_recipe_in_batch(self, qtd=10):
        recipes = []
        for i in range(qtd):
            kwargs = {
                'recipe_title': f'Recipe Title {i}',
                'recipe_slug': f'r{i}',
                'recipe_author': {'author_username': f'u{i}'}
            }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()

