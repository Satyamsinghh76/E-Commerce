from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from cart.models import Cart, CartItem
from products.models import Category, Product
from .models import Order


class OrderAPITests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user('anshika', 'anshika@example.com', 'test12345')
		self.other_user = User.objects.create_user('rahul', 'rahul@example.com', 'test12345')
		self.client.force_authenticate(user=self.user)

		self.category = Category.objects.create(name='Jeans')
		self.product = Product.objects.create(
			name='Slim Fit Jeans',
			description='Blue denim',
			price='1999.00',
			stock=10,
			category=self.category,
		)

	def _add_item_to_cart(self, quantity=2):
		cart, _ = Cart.objects.get_or_create(user=self.user)
		CartItem.objects.create(cart=cart, product=self.product, quantity=quantity)
		return cart

	def test_place_order_success(self):
		self._add_item_to_cart(quantity=2)
		response = self.client.post('/api/orders/', {'shipping_address': 'Noida, UP'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data['status'], 'PENDING')
		self.product.refresh_from_db()
		self.assertEqual(self.product.stock, 8)

	def test_place_order_with_empty_cart_fails(self):
		response = self.client.post('/api/orders/', {'shipping_address': 'Noida, UP'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_list_only_own_orders(self):
		self._add_item_to_cart(quantity=1)
		self.client.post('/api/orders/', {'shipping_address': 'Noida, UP'}, format='json')

		other_order = Order.objects.create(
			user=self.other_user,
			status='PENDING',
			total_price='99.00',
			shipping_address='Delhi'
		)

		response = self.client.get('/api/orders/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)
		self.assertNotEqual(response.data[0]['id'], other_order.id)

	def test_cancel_order_restores_stock(self):
		self._add_item_to_cart(quantity=3)
		place_response = self.client.post('/api/orders/', {'shipping_address': 'Noida, UP'}, format='json')
		order_id = place_response.data['id']

		cancel_response = self.client.post(f'/api/orders/{order_id}/cancel/')
		self.assertEqual(cancel_response.status_code, status.HTTP_200_OK)
		self.assertEqual(cancel_response.data['status'], 'CANCELLED')

		self.product.refresh_from_db()
		self.assertEqual(self.product.stock, 10)
