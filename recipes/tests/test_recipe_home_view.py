from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):

    # Testes para Home ---------------------------------------------------------
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertIn(
            "No recipes found here 😢", response.content.decode("utf-8")
        )

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode("utf-8")
        response_context_recipes = response.context["recipes"]
        # Check if one recipe exists
        self.assertIn("Recipe Title", content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        # Need a recipe for this test
        self.make_recipe(is_published=False)

        response = self.client.get(reverse("recipes:home"))

        # Check if one recipe exists
        self.assertIn(
            "No recipes found here 😢", response.content.decode("utf-8")
        )

    # Teste para saber se a quantidade de receita criada é igual a quantidade
    # de receitas mostrada na pagina
    def test_recipe_home_template_shows_amount_recipes_found(self):
        # Creates 15 recipes
        for i in range(15):
            self.make_recipe(
                title=f"Recipe {i}",
                slug=f"recipe-slug-{i}",
                author_data={"username": f"username{i}"},
            )
        # Aqui eu quero q mostra 8 receitas na pagina com o new=8
        with patch("recipes.views.PER_PAGE", new=8):
            response = self.client.get(reverse("recipes:home"))
            recipes = response.context["recipes"]
            self.assertEqual(len(recipes), 8)

    # Mesmo teste de antes porem pra saber quanto mostra na proxima pagina
    def test_recipe_home_template_shows_amount_recipes_found_in_second_page(
        self,
    ):
        # Creates 15 recipes
        for i in range(15):
            self.make_recipe(
                title=f"Recipe {i}",
                slug=f"recipe-slug-{i}",
                author_data={"username": f"username{i}"},
            )
        # Aqui quero que mostra quantas receitas tem na segunda pagina
        with patch("recipes.views.PER_PAGE", new=8):
            response = self.client.get(reverse("recipes:home") + "?page=2")
            recipes = response.context["recipes"]
            self.assertEqual(len(recipes), 7)

    # Teste pra saber a quantidade de paginas geradas por receitas criadas
    def test_recipe_home_is_paginated(self):
        for i in range(15):
            kwargs = {
                "title": f"Recipe {i}",
                "slug": f"recipe-slug-{i}",
                "author_data": {"username": f"username{i}"},
            }
            self.make_recipe(**kwargs)
        # Aqui o teste é de paginacao, mais pra saber
        # quantas paginas gerou com o numero de receita criado
        with patch("recipes.views.PER_PAGE", new=4):
            response = self.client.get(reverse("recipes:home"))
            recipes = response.context["recipes"]
            paginator = recipes.paginator
            self.assertEqual(paginator.num_pages, 4)
            self.assertEqual(len(paginator.get_page(1)), 4)
            self.assertEqual(len(paginator.get_page(2)), 4)
            self.assertEqual(len(paginator.get_page(3)), 4)
            self.assertEqual(len(paginator.get_page(4)), 3)

    def test_invalid_page_query_uses_page_one(self):
        for i in range(15):
            kwargs = {
                "title": f"Recipe {i}",
                "slug": f"recipe-slug-{i}",
                "author_data": {"username": f"username{i}"},
            }
            self.make_recipe(**kwargs)

        with patch("recipes.views.PER_PAGE", new=4):
            response = self.client.get(reverse("recipes:home") + "?page=1A")
            self.assertEqual(response.context["recipes"].number, 1)

            response = self.client.get(reverse("recipes:home") + "?page=2")
            self.assertEqual(response.context["recipes"].number, 2)

            response = self.client.get(reverse("recipes:home") + "?page=3")
            self.assertEqual(response.context["recipes"].number, 3)
