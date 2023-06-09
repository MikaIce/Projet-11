""" This file contains all Tests about Purbeurre app """
from django.test import TestCase
from django.urls import reverse


class TestPurbeurre(TestCase):
    """Test all User Purbeurre views"""

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_legal_view(self):
        response = self.client.get(reverse('legal'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'legal.html')

    def test_404_view(self):
        response = self.client.get('/test404')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '404.html')