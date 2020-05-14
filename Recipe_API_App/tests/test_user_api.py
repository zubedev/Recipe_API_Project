"""test_user_api.py"""

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('api:create_user')
CREATE_TOKEN_URL = reverse('api:create_token')
ME_URL = reverse('api:me')


def create_user(**kwargs):
    """create_user helper function"""
    return get_user_model().objects.create_user(**kwargs)


class PublicUserAPITests(TestCase):
    """Tests the public users API"""

    def setUp(self):
        """setup"""
        self.client = APIClient()

    def test_create_user_api(self):
        """Tests create_user API"""
        data = {
            'email': 'test_user@email.com',
            'password': 'TestPass123#',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, data=data)
        user = get_user_model().objects.get(**res.data)

        # assert
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(data['password']))
        self.assertNotIn('password', res.data)  # make sure password not return

    def test_create_user_exists(self):
        """Tests create_user for duplicate user or user exists"""
        data = {
            'email': 'Test_User@ZuBe.dev',
            'password': 'password',
        }
        create_user(**data)  # make user exist
        with self.assertRaises(Exception) as raised:
            self.client.post(CREATE_USER_URL, data=data)  # duplication

        # assert
        self.assertEqual(type(raised.exception), IntegrityError)

    def test_create_user_password_length(self):
        """Tests password length of minimum 8 characters while creating user"""
        data = {
            'email': 'test@email.net',
            'password': '1234567',
        }
        res = self.client.post(CREATE_USER_URL, data=data)
        user_exists = get_user_model().objects.filter(email=data['email'])\
            .exists()

        # assert
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user_exists)  # user not created

    def test_token_for_user(self):
        """Tests that token is returned for user"""
        data = {
            'email': 'user@ZuBe.dev',
            'password': 'password'
        }
        create_user(**data)
        res = self.client.post(CREATE_TOKEN_URL, data=data)

        # assert
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)  # token should be returned

    def test_token_for_invalid_creds(self):
        """Tests that token is not returned for invalid credentials"""
        create_user(email='user@email.com', password='password')
        data = {'email': 'user@email.com', 'password': 'incorrect'}
        res = self.client.post(CREATE_TOKEN_URL, data=data)

        # assert
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)  # no token should be returned

    def test_token_for_no_user(self):
        """Tests that token is not returned for no or invalid user"""
        data = {
            'email': 'user@zube.dev',
            'password': 'passpass'
        }
        res = self.client.post(CREATE_TOKEN_URL, data=data)

        # assert
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)  # not token should be returned

    def test_token_missing_field(self):
        """Tests that token is not returned for incomplete data"""
        data = {'email': 'user@mail.net', 'password': ''}
        res = self.client.post(CREATE_TOKEN_URL, data=data)

        # assert
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_unauthorized_user_retrieval(self):
        """Tests that authentication is required for users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        """setup"""
        self.user = create_user(
            email="testuser@zube.dev",
            password="password",
            name="Test User"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_user_profile_retrieval(self):
        """Tests retrieval of profile for authenticated user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {'name': self.user.name,
                                    'email': self.user.email})

    def test_post_not_allowed_on_me(self):
        """Tests that POST is not allowed on Me URL"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Tests that user profile can be updated for authenticated user"""
        data = {'name': 'New Name', 'password': 'testpass'}
        res = self.client.patch(ME_URL, data=data)
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, data['name'])
        self.assertTrue(self.user.check_password(data['password']))
