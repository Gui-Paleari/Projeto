from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):

    # Testes para Category -----------------------------------------------------
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse("recipes:category", kwargs={"category_id": 1000})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_is_no_recipes_found(self):
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = "This is a category test"

        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse("recipes:category", args=(1,)))
        content = response.content.decode("utf-8")

        # Check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse("recipes:recipe", kwargs={"id": recipe.category.id})
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_shows_amount_recipes_found(self):
        category = self.make_category(name="Category Teste")
        # Creates 15 recipes
        for i in range(15):
            recipe = self.make_recipe(
                title=f"Recipe {i}",
                slug=f"recipe-slug-{i}",
                author_data={"username": f"username{i}"},
            )
            recipe.category = category
            recipe.save()
        # Check if the number of recipes per page has been loaded correctly
        with patch("recipes.views.PER_PAGE", new=9):
            response = self.client.get(
                reverse("recipes:category", args=(category.id,))
            )
            recipes = response.context["recipes"]
            self.assertEqual(len(recipes), 9)

    def test_recipe_category_template_shows_amount_recipes_found_in_second_page(
        self,
    ):
        category = self.make_category(name="Category Teste")
        # Creates 15 recipes
        for i in range(15):
            recipe = self.make_recipe(
                title=f"Recipe {i}",
                slug=f"recipe-slug-{i}",
                author_data={"username": f"username{i}"},
            )
            recipe.category = category
            recipe.save()
        with patch("recipes.views.PER_PAGE", new=9):
            # Check if the number of recipes on the second page has loaded correctly
            response = self.client.get(
                reverse("recipes:category", args=(category.id,)) + "?page=2"
            )
            recipes = response.context["recipes"]
            self.assertEqual(len(recipes), 6)
