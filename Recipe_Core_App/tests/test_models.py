"""Tests Recipe Core App Models"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from Recipe_Core_App import models


def sample_user(email="user@sample.com", password="samplepwd"):
    """Sample user to be used for tests"""
    return get_user_model().objects.create_user(email, password)


class ModelsTest(TestCase):
    """Aggregated Test Class for all Recipe Core App Models"""
    UserModel = get_user_model()

    def test_create_user(self):
        """Tests create_user with email address and password"""
        # setup
        email = "admin@ZuBe.dev"
        password = "Admin123#"

        # run
        user = self.UserModel.objects.create_user(
            email=email,
            password=password
        )

        # assert
        self.assertEqual(user.email, email.lower())  # checks normalization
        self.assertNotEqual(user.password, password)  # checks for plain-text
        self.assertTrue(user.check_password(password))  # checks password

    def test_create_user_with_no_email(self):
        """Tests create_user with no email address provided by user"""
        # setup with no email variable
        password = "admin123"

        # run/assert
        with self.assertRaises(ValueError):  # using email=""
            self.UserModel.objects.create_user("", password=password)
        with self.assertRaises(ValueError):  # using email=None
            self.UserModel.objects.create_user(None, password=password)

    def test_create_user_status(self):
        """Tests create_user staff and superuser status"""
        # setup
        email = "admin@zube.dev"
        password = "notstafforsuperuser"

        # run
        user = self.UserModel.objects.create_user(email, password)

        # assert
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        """Tests create_superuser functionality"""
        # setup
        email = "admin@zube.dev"
        password = "superuser"

        # run
        user = self.UserModel.objects.create_superuser(
            email=email,
            password=password
        )

        # assert
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Tests the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vegan"
        )
        self.assertEqual(tag.name, str(tag))

    def test_ingredient_str(self):
        """Tests the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Cucumber"
        )
        self.assertEqual(ingredient.name, str(ingredient))
