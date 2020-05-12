"""Tests Recipe Core App Admin"""

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Admin Site Test class"""
    UserModel = get_user_model()

    def setUp(self):
        """Test setup"""
        self.client = Client()
        self.superuser = self.UserModel.objects.create_superuser(
            email="superuser@ZuBe.dev",
            password="SuperDuperUser123#",
            name="Admin User"
        )
        self.client.force_login(self.superuser)
        self.user = self.UserModel.objects.create_user(
            email="testuser@email.net",
            password="Password123",
            name="Test User"
        )

    # for admin site reverse urls, please check the following documentation
    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#reversing-admin-urls

    def test_user_list(self):
        """Tests that users are listed on admin user list page"""
        # setup
        url = reverse("admin:Recipe_Core_App_customuser_changelist")
        res = self.client.get(url)

        # assert
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change(self):
        """Tests that users are editable on admin site"""
        # setup
        url = reverse(
            "admin:Recipe_Core_App_customuser_change",
            args=[self.user.id]
        )
        res = self.client.get(url)

        # assert
        self.assertEqual(res.status_code, 200)

    def test_create_user(self):
        """Tests that users can be created on admin site"""
        # setup
        url = reverse("admin:Recipe_Core_App_customuser_add")
        res = self.client.get(url)

        # assert
        self.assertEqual(res.status_code, 200)
