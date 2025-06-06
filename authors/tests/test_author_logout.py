from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username="my_user", password="my_pass")
        self.client.login(username="my_user", password="my_pass")

        response = self.client.get(reverse("authors:logout"), follow=True)

        self.assertIn(
            "Invalid logout request", response.content.decode("utf-8")
        )

    def test_user_tries_to_logout_another_user(self):
        # sourcery skip: class-extract-method
        User.objects.create_user(username="my_user", password="my_pass")
        self.client.login(username="my_user", password="my_pass")

        response = self.client.post(
            reverse("authors:logout"),
            data={"username": "another_user"},
            follow=True,
        )

        self.assertIn("Invalid logout user", response.content.decode("utf-8"))

    def test_user_can_logout_successfully(self):
        User.objects.create_user(username="my_user", password="my_pass")
        self.client.login(username="my_user", password="my_pass")

        response = self.client.post(
            reverse("authors:logout"), data={"username": "my_user"}, follow=True
        )

        self.assertIn(
            "Logged out successfully", response.content.decode("utf-8")
        )
