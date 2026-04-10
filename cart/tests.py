from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Category, Product
from .models import CartItem


class CartAPITests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user('anshika', 'anshika@example.com', 'test12345')
		self.client.force_authenticate(user=self.user)
		self.category = Category.objects.create(name='T-Shirts')
		self.product = Product.objects.create(
			name='Graphic Tee',
			description='100% cotton',
			price='999.00',
			stock=5,
			category=self.category,
		)

	def test_add_to_cart_creates_item(self):
		response = self.client.post('/api/cart/', {'product_id': self.product.id, 'quantity': 2}, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['total_items'], 1)
		self.assertEqual(response.data['items'][0]['quantity'], 2)

	def test_add_same_product_merges_quantity(self):
		self.client.post('/api/cart/', {'product_id': self.product.id, 'quantity': 1}, format='json')
		response = self.client.post('/api/cart/', {'product_id': self.product.id, 'quantity': 2}, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['items'][0]['quantity'], 3)
		self.assertEqual(CartItem.objects.count(), 1)

	def test_add_to_cart_rejects_excess_stock(self):
		response = self.client.post('/api/cart/', {'product_id': self.product.id, 'quantity': 10}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_update_and_remove_cart_item(self):
		add_response = self.client.post('/api/cart/', {'product_id': self.product.id, 'quantity': 1}, format='json')
		item_id = add_response.data['items'][0]['id']

		patch_response = self.client.patch(f'/api/cart/item/{item_id}/', {'quantity': 4}, format='json')
		self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
		self.assertEqual(patch_response.data['items'][0]['quantity'], 4)

		delete_response = self.client.delete(f'/api/cart/item/{item_id}/')
		self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
		self.assertEqual(delete_response.data['total_items'], 0)
