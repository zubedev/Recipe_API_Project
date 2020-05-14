"""test_ingredient_api.py"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from Recipe_Core_App.models import Ingredient
from Recipe_API_App.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('api:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """Test the publically available ingredients API"""

    def setUp(self):
        """setup"""
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITests(TestCase):
    """Test ingredients can be retrieved by authorized user"""

    def setUp(self):
        """setup"""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@ZuBe.dev',
            password='password'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that only ingredients for authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'user2@zube.dev',
            'testpass'
        )
        Ingredient.objects.create(user=user2, name='Vinegar')

        ingredient = Ingredient.objects.create(user=self.user, name='Turmeric')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """Test creating a new ingredient"""
        data = {'name': 'Cabbage'}
        self.client.post(INGREDIENTS_URL, data=data)

        ingredient_exists = Ingredient.objects.filter(
            user=self.user,
            name=data['name']
        ).exists()
        self.assertTrue(ingredient_exists)

    def test_create_ingredient_invalid(self):
        """Test creating invalid ingredient fails"""
        data = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, data=data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
