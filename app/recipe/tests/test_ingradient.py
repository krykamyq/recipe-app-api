""""Test for Ingradient API"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingradient

from recipe.serializers import IngradientSerializer


INGRAGIENT_URL = reverse('recipe:ingradient-list')


def detail_ingradient(ingradient_id):
    return reverse('recipe:ingradient-detail', args=[ingradient_id])


class PublicIngradientApiTests(TestCase):
    """Test the publicly available Ingradients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(INGRAGIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngradientApiTests(TestCase):
    """Test the private Ingradients API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingradients(self):
        """Test retrieving a list of ingradients"""
        Ingradient.objects.create(
            user=self.user,
            name='Ingradient 1',
        )
        Ingradient.objects.create(
            user=self.user,
            name='Ingradient 2',
        )

        res = self.client.get(INGRAGIENT_URL)

        ingradients = Ingradient.objects.all().order_by('-name')
        serializer = IngradientSerializer(ingradients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingradients_limited_to_user(self):
        """Test that ingradients for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'test2@example.com',
            'testpass123'
        )
        Ingradient.objects.create(
            user=user2,
            name='Ingradient 1',
        )
        ingradient = Ingradient.objects.create(
            user=self.user,
            name='Ingradient 2',
        )

        res = self.client.get(INGRAGIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingradient.name)
        self.assertEqual(res.data[0]['id'], ingradient.id)

    def test_update_ingradient_successful(self):
        """Test updating an ingradient's name"""
        ingradient = Ingradient.objects.create(
            user=self.user,
            name='Ingradient 1',
        )

        payload = {'name': 'Updated Ingradient'}
        url = detail_ingradient(ingradient.id)
        self.client.patch(url, payload)

        ingradient.refresh_from_db()
        self.assertEqual(ingradient.name, payload['name'])

    def test_delete_ingradient_successful(self):
        """Test deleting an ingradient"""
        ingradient = Ingradient.objects.create(
            user=self.user,
            name='Ingradient 1',
        )

        url = detail_ingradient(ingradient.id)
        self.client.delete(url)

        with self.assertRaises(Ingradient.DoesNotExist):
            Ingradient.objects.get(id=ingradient.id)
