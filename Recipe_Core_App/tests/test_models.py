"""Tests Recipe Core App Models"""

from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelsTest(TestCase):
    """Aggregated Test Class for all Recipe Core App Models"""

    def test_create_user(self):
        """Tests create_user with email address and password"""
        # setup
        email = "admin@zube.dev"
        password = "Admin123#"

        # run
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        # assert
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
