from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegistrationTests(TestCase):
    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": "teacher1@example.com",
                "password1": "SuperTajneHaslo123",
                "password2": "SuperTajneHaslo123",
            },
        )
        self.assertRedirects(response, reverse("panel"))
        user = User.objects.get(email="teacher1@example.com")
        self.assertEqual(user.username, "teacher1@example.com")

        panel = self.client.get(reverse("panel"))
        self.assertContains(panel, "teacher1@example.com")

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user(username="teacher1@example.com", email="teacher1@example.com", password="x")
        response = self.client.post(
            reverse("register"),
            {
                "email": "teacher1@example.com",
                "password1": "SuperTajneHaslo123",
                "password2": "SuperTajneHaslo123",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "email", "Konto z tym adresem email już istnieje.")


class LoginLogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teacher1@example.com", email="teacher1@example.com", password="SuperTajneHaslo123"
        )

    def test_login_with_email(self):
        response = self.client.post(
            reverse("login"), {"username": "teacher1@example.com", "password": "SuperTajneHaslo123"}
        )
        self.assertRedirects(response, reverse("panel"))

    def test_panel_requires_login(self):
        response = self.client.get(reverse("panel"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('panel')}")

    def test_logout_redirects_to_login(self):
        self.client.login(username="teacher1@example.com", password="SuperTajneHaslo123")
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
        self.assertEqual(self.client.get(reverse("panel")).status_code, 302)
