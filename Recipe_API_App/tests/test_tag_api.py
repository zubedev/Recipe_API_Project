"""test_tag_api.py"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from Recipe_Core_App.models import Tag
from Recipe_API_App.serializers import TagSerializer


TAGS_URL = reverse('api:tag-list')


class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        """setup"""
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving tags"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        """setup"""
        self.user = get_user_model().objects.create_user(
            email='testuser@zube.dev',
            password='password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')
        tags = Tag.objects.all().order_by('name')
        serializer = TagSerializer(tags, many=True)
        # request/response
        res = self.client.get(TAGS_URL)
        # test/assert
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            email='user2@ZuBe.dev',
            password='testpass'
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')
        # request/response
        res = self.client.get(TAGS_URL)
        # test/assert
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        data = {'name': 'Simple'}
        self.client.post(TAGS_URL, data=data)

        tag_exists = Tag.objects.filter(
            user=self.user,
            name=data['name']
        ).exists()

        self.assertTrue(tag_exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid data"""
        data = {'name': ''}
        res = self.client.post(TAGS_URL, data=data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
