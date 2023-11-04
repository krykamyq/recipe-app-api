"""Test for recipe API"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer
)


RECIPE_URL = reverse('recipe:recipe-list')


def detial_url(recipe_id):
    """Create and return url for detail recipe."""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params):
    """Create recipe for tests."""

    defaults = {
        'title': 'Simple recipe',
        'time_minutes': 22,
        'price': Decimal(5.50),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf'
    }

    defaults.update(params)

    res = Recipe.objects.create(user=user, **defaults)

    return res


class PublicRecipeAPITests(TestCase):
    """Test for unauthenticadet API requests."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITest(TestCase):
    """Test for authenticadet API requests."""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='test123',
            name='Test name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retriving_list_recipe(self):
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limmited_to_user(self):
        """Test list of recipes is limited for authenticated user."""

        other_user = get_user_model().objects.create_user(
            email='other@example.com',
            password='test123',
        )
        create_recipe(user=self.user)
        create_recipe(user=other_user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test recipe details"""
        recipe = create_recipe(user=self.user)

        url = detial_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """"Test recipe is created"""

        payloud = {
            'title': 'Test',
            'time_minutes': 5,
            'price': Decimal('5.50'),
        }
        res = self.client.post(RECIPE_URL, payloud)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in payloud.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update_recipe(self):
        recipe = create_recipe(user=self.user)
        data = {'title': 'Updated Recipe Title'}
        url = detial_url(recipe.id)
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the data has been updated in the database
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, data['title'])
        self.assertEqual(recipe.link, 'http://example.com/recipe.pdf')
        self.assertEqual(recipe.user, self.user)

    def test_full_update_recipe(self):
        recipe = create_recipe(user=self.user)

        payload = {
            'title': 'New Title',
            'description': 'New sample of description',
            'price': Decimal('12.30'),
            'time_minutes': 30,
            'link': 'https://example2.com/recipe.pdf'
        }

        url = detial_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_update_user_faild(self):
        new_user = get_user_model().objects.create_user(
            email='test2@example.com',
            password='test123')
        recipe = create_recipe(user=self.user)
        payload = {'user': new_user.id}

        url = detial_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        recipe = create_recipe(user=self.user)

        url = detial_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_recipe_other_user_recipe_error(self):
        new_user = get_user_model().objects.create_user(
            email='test2@example.com',
            password='test123')
        recipe = create_recipe(user=new_user)

        url = detial_url(recipe.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())
