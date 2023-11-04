from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Tags


class TagAPITest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            email='testuser',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

        # Create some tags
        self.tag1 = Tags.objects.create(name='Tag 1', user=self.user)
        self.tag2 = Tags.objects.create(name='Tag 2', user=self.user)

        self.urltag = reverse('recipe:tags-detail', args=[self.tag1.id])
        self.url = reverse('recipe:tags-list')

    def test_authenticated_access(self):
        # Simulate an authenticated request
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_tags(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_tag(self):
        response = self.client.get(self.urltag)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_tag(self):
        data = {
            'name': 'New Tag'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_tag(self):
        data = {
            'name': 'Updated Tag',
        }
        response = self.client.put(self.urltag, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tag1.refresh_from_db()
        self.assertEqual(self.tag1.name, 'Updated Tag')

    def test_delete_tag(self):
        response = self.client.delete(self.urltag)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tags.objects.count(), 1)
