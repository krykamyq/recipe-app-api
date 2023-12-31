"""
Tests for the tags API.
"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tags, Recipe

from recipe.serializers import TagsSerializer


TAGS_URL = reverse('recipe:tags-list')


def detail_url(tag_id):
    """Create and return a tag detail url."""
    return reverse('recipe:tags-detail', args=[tag_id])


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicTagsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving tags."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving a list of tags."""
        Tags.objects.create(user=self.user, name='Vegan')
        Tags.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tags.objects.all().order_by('-name')
        serializer = TagsSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test list of tags is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Tags.objects.create(user=user2, name='Fruity')
        tag = Tags.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_tag(self):
        """Test updating a tag."""
        tag = Tags.objects.create(user=self.user, name='After Dinner')

        payload = {'name': 'Dessert'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """Test deleting a tag."""
        tag = Tags.objects.create(user=self.user, name='Breakfast')

        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tags.objects.filter(user=self.user)
        self.assertFalse(tags.exists())

    def test_tags_assigned_to_recipes(self):
        """Test filtering tags by those assigned to recipes."""
        tag1 = Tags.objects.create(user=self.user, name='Vegan')
        tag2 = Tags.objects.create(user=self.user, name='Dessert')
        recipe = Recipe.objects.create(
            user=self.user,
            title='Test Recipe',
            time_minutes=10,
            price=Decimal(10),
            description='Test Description',)
        recipe.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})
        serializer1 = TagsSerializer(tag1)
        serializer2 = TagsSerializer(tag2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_tags_assigned_unique(self):
        """Test filtering tags by assigned returns unique items."""
        tag1 = Tags.objects.create(user=self.user, name='Vegan')
        Tags.objects.create(user=self.user, name='Dessert')
        recipe1 = Recipe.objects.create(
            user=self.user,
            title='Test Recipe',
            time_minutes=10,
            price=Decimal(10),
            description='Test Description',)
        recipe2 = Recipe.objects.create(
            user=self.user,
            title='Test Recipe2',
            time_minutes=10,
            price=Decimal(10),
        )
        recipe1.tags.add(tag1)
        recipe2.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)
