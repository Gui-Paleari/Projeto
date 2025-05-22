# flake8: noqa
# from django.test import LiveServerTestCase (Nao contem arquivos estáticos por
# ser feito para testar apenas lógica)

import time

# Metodo para mostrar o navegador todo estilizado com arquivos estáticos
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from recipes.tests.test_recipe_base import RecipeMixin
from utils.browser import make_chrome_browser


class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=8):
        time.sleep(seconds)
