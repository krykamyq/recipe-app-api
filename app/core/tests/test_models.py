"""
Tests for models.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email="test@example.com", password="test123"):
    return get_user_model().objects.create_user(email, password)


class MotelTest(TestCase):
    """Test models."""
    def test_create_user_with_email_successful(self):
        """Test createing user with email is successful"""

        email = 'test@example.com'
        password = 'password123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_emails = [
            ['test1@example.com', 'test1@example.com'],
            ['TEST2@example.com', 'TEST2@example.com'],
            ['Test3@example.com', 'Test3@example.com'],
            ['test4@EXAMPLE.com', 'test4@example.com'],
            ['test5@example.COM', 'test5@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='testpass123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'password1234')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test for create recipe model."""
        user = get_user_model().objects.create_user(
            'test@example@com',
            'test123',
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Simple recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Simple recipe description',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tags(self):
        """Test for create tags model."""
        user = create_user()
        tag = models.Tags.objects.create(name='New Tag', user=user)

        self.assertEqual(str(tag), tag.name)

    def test_create_ingradint(self):
        """Test for create ingradint."""
        user = create_user()
        ingradient = models.Ingradient.objects.create(
            name='New Ingradient', user=user)
        self.assertEqual(str(ingradient), ingradient.name)
