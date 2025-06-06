import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest

User = get_user_model()


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = "pass"
        user = User.objects.create_user(
            username="my_user", password=string_password
        )

        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse("authors:login"))

        # Usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, "main-form")
        username_field = self.get_by_placeholder(form, "Type your username")
        password_field = self.get_by_placeholder(form, "Type your password")

        # Usuário digita seu usuário e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # Usuário envia o formulário
        form.submit()

        # Usuário vê a mensagem de login com sucesso e seu nome
        self.assertIn(
            f"You are logged in with {user.username}.",
            self.browser.find_element(By.TAG_NAME, "body").text,
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse("authors:login_create"))

        self.assertIn(
            "Not Found",
            self.browser.find_element(By.TAG_NAME, "body").text,
        )

    def test_form_login_invalid_credential(self):
        string_password = "pass"

        user = User.objects.create_user(
            username="my_user", password=string_password
        )

        self.browser.get(self.live_server_url + reverse("authors:login"))

        form = self.browser.find_element(By.CLASS_NAME, "main-form")
        username_field = self.get_by_placeholder(form, "Type your username")
        password_field = self.get_by_placeholder(form, "Type your password")

        # Enviou com algum caracter errado que não corresponde
        username_field.send_keys("my_userrr")
        password_field.send_keys(string_password)

        form.submit()

        self.assertIn(
            "Invalid credentials.",
            self.browser.find_element(By.TAG_NAME, "body").text,
        )

    def test_form_login_is_invalid(self):
        self.browser.get(self.live_server_url + reverse("authors:login"))

        form = self.browser.find_element(By.CLASS_NAME, "main-form")

        username_field = self.get_by_placeholder(form, "Type your username")
        password_field = self.get_by_placeholder(form, "Type your password")

        # Enviou os campos no input vazio
        username_field.send_keys(" ")
        password_field.send_keys(" ")

        form.submit()

        self.assertIn(
            "Invalid username or password.",
            self.browser.find_element(By.TAG_NAME, "body").text,
        )
