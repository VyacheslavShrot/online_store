import unittest

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class TestAuthUser(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.user = get_user_model().objects.create(username="user_test")
        self.user.set_password("123456789")
        self.user.save()

        self.admin = get_user_model().objects.create(username="admin_test", is_staff=True)
        self.admin.set_password("123456789")
        self.admin.save()

    def test_user_login_wrong_username(self):
        user_login = self.client.login(username="wrong_username", password="123456789")
        self.assertFalse(user_login)

    def test_user_login_wrong_password(self):
        user_login = self.client.login(username="user_test", password="1")
        self.assertFalse(user_login)

    def test_user_access_admin_panel(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)

    def test_admin_access_admin_panel(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)

    @unittest.skip("Don't have index page yet")
    def test_user_access(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
