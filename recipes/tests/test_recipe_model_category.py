from parameterized import parameterized
from django.core.exceptions import ValidationError

from recipes.tests.test_recipe_base import RecipeTestBase, Category


class CategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category()
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    @parameterized.expand([
        ('name', 65)
    ])
    def test_category_fields_max_length(self, field, max_length):
        setattr(self.category, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_category_string_representation(self):
        needed = 'Testing Representation'
        self.category.name = needed
        self.category.full_clean()
        self.category.save()
        self.assertEqual(
            str(self.category), needed,
            msg=f'Category string representation must be '
                f'"{needed}" but "{str(self.category)}" was received.'
        )
