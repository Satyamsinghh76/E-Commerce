from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Product


class ProductAPITests(APITestCase):
	def setUp(self):
		self.category = Category.objects.create(name='Shoes')
		Product.objects.create(
			name='Nike Air',
			description='Running shoe',
			price='4999.00',
			stock=10,
			category=self.category,
		)
		Product.objects.create(
			name='Adidas Ultraboost',
			description='Comfort shoe',
			price='5999.00',
			stock=8,
			category=self.category,
		)
		self.user = User.objects.create_user('anshika', 'anshika@example.com', 'test12345')
		self.admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')

	def test_public_can_list_products(self):
		response = self.client.get('/api/products/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data['results']), 2)

	def test_search_products(self):
		response = self.client.get('/api/products/?search=nike')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data['results']), 1)
		self.assertEqual(response.data['results'][0]['name'], 'Nike Air')

	def test_non_admin_cannot_create_product(self):
		self.client.force_authenticate(user=self.user)
		response = self.client.post('/api/products/', {
			'name': 'Puma Runner',
			'price': '2999.00',
			'stock': 5,
			'category': self.category.id,
		}, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_admin_can_create_product(self):
		self.client.force_authenticate(user=self.admin)
		response = self.client.post('/api/products/', {
			'name': 'Puma Runner',
			'price': '2999.00',
			'stock': 5,
			'category': self.category.id,
		}, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(Product.objects.filter(name='Puma Runner').exists())
