from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):

    # Testes para Search -------------------------------------------------------
    def test_recipe_search_uses_correct_view_function(self):
        url = reverse("recipes:search")
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse("recipes:search") + "?q=teste")
        self.assertTemplateUsed(response, "recipes/pages/search.html")

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse("recipes:search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse("recipes:search") + "?q=<Teste>"
        response = self.client.get(url)
        self.assertIn(
            "Search for &#x27;&lt;Teste&gt;&#x27;",
            response.content.decode("utf-8"),
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = "This is recipe one"
        title2 = "This is recipe two"

        recipe1 = self.make_recipe(
            slug="one", title=title1, author_data={"username": "one"}
        )
        recipe2 = self.make_recipe(
            slug="two", title=title2, author_data={"username": "two"}
        )

        search_url = reverse("recipes:search")
        response1 = self.client.get(f"{search_url}?q={title1}")
        response2 = self.client.get(f"{search_url}?q={title2}")
        response_both = self.client.get(f"{search_url}?q=this")

        self.assertIn(recipe1, response1.context["recipes"])
        self.assertNotIn(recipe2, response1.context["recipes"])

        self.assertIn(recipe2, response2.context["recipes"])
        self.assertNotIn(recipe1, response2.context["recipes"])

        self.assertIn(recipe1, response_both.context["recipes"])
        self.assertIn(recipe2, response_both.context["recipes"])

    def test_recipe_search_if_shows_amount_recipes_found(self):
        # Creates 15 recipes com títulos variados
        recipes_all = []
        for i in range(15):
            if i in [1, 3, 7, 10, 11]:
                # Títulos personalizados
                custom_titles = {
                    1: "Bolo de pistache",
                    3: "Bolo de cenoura",
                    7: "Macarrão com queijo",
                    10: "Pizza de calabresa",
                    11: "Pizza de frango",
                }
                title = custom_titles[i]
            else:
                title = f"Essa é a receita {i}"

            recipes_all1 = self.make_recipe(
                title=title,
                slug=f"recipe-slug-{i}",
                author_data={"username": f"username{i}"},
            )
            recipes_all.append(recipes_all1)
        with patch("recipes.views.PER_PAGE", new=9):

            search_url = reverse("recipes:search")

            response__1 = self.client.get(f"{search_url}?q=pizza de")
            recipes__1 = response__1.context["recipes"]

            response__2 = self.client.get(
                f"{search_url}?q=essa é a receita&page=1"
            )  # ou ?q=essa é a receita"
            recipes__2 = response__2.context["recipes"]

            response__2_1 = self.client.get(
                f"{search_url}?q=essa é a receita&page=2"
            )
            recipes__2_1 = response__2_1.context["recipes"]

            response__3 = self.client.get(f"{search_url}?q=Bolo de pistache")

            self.assertEqual(len(recipes_all), 15)
            self.assertEqual(len(recipes__1), 2)
            self.assertEqual(len(recipes__2), 9)
            self.assertEqual(len(recipes__2_1), 1)
            self.assertIn(recipes_all[1], response__3.context["recipes"])
