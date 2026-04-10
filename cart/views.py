"""
Cart Views — Phase 3

EDGE CASES handled:
  1. Adding same product twice → UPDATE quantity (not duplicate row)
  2. Adding more than available stock → 400 error
  3. Quantity update exceeds stock → 400 error
  4. Removing item that doesn't belong to user's cart → 404
  5. Cart auto-created on first access → no separate "create cart" endpoint needed

WHY APIView instead of ModelViewSet?
Cart behavior doesn't map cleanly to standard CRUD — we have custom logic
for add/update/remove. APIView gives explicit HTTP method control.
"""
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import CartSerializer, AddToCartSerializer, UpdateCartItemSerializer
from products.models import Product


class CartView(APIView):
    """
    GET  /api/cart/  → View current cart
    POST /api/cart/  → Add item to cart
    """
    permission_classes = [permissions.IsAuthenticated]

    def _get_or_create_cart(self, user):
        """Helper: lazily creates cart on first access."""
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def get(self, request):
        cart = self._get_or_create_cart(request.user)
        # prefetch to avoid N+1 queries for items and their products
        cart = Cart.objects.prefetch_related('items__product').get(id=cart.id)
        return Response(CartSerializer(cart).data)

    def post(self, request):
        """Add product to cart. Handles duplicates gracefully."""
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity   = serializer.validated_data['quantity']

        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Edge Case 1: Not enough stock to add requested quantity
        if product.stock < quantity:
            return Response(
                {'error': f'Only {product.stock} item(s) available in stock.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = self._get_or_create_cart(request.user)

        # get_or_create: if product already in cart → returns existing item + created=False
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            # Edge Case 2: Product already in cart — add to existing quantity
            new_qty = cart_item.quantity + quantity
            if new_qty > product.stock:
                return Response(
                    {'error': f'Cannot add {quantity} more. Max available: {product.stock}. You already have {cart_item.quantity} in cart.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_qty
            cart_item.save()

        # Refresh cart with prefetch for clean response
        cart = Cart.objects.prefetch_related('items__product').get(id=cart.id)
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    def delete(self, request):
        """DELETE /api/cart/ → Clear entire cart"""
        cart = self._get_or_create_cart(request.user)
        cart.items.all().delete()
        return Response({'message': 'Cart cleared successfully.'}, status=status.HTTP_200_OK)


class CartItemView(APIView):
    """
    PATCH  /api/cart/item/{item_id}/  → Update quantity
    DELETE /api/cart/item/{item_id}/  → Remove single item
    """
    permission_classes = [permissions.IsAuthenticated]

    def _get_cart_item(self, item_id, user):
        """
        Fetch cart item — ensures it belongs to the requesting user.
        cart__user=user prevents one user from modifying another's cart!
        """
        try:
            return CartItem.objects.select_related('product', 'cart').get(
                id=item_id, cart__user=user
            )
        except CartItem.DoesNotExist:
            return None

    def patch(self, request, item_id):
        """Update quantity of a specific cart item."""
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = self._get_cart_item(item_id, request.user)
        if not item:
            return Response({'error': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

        new_qty = serializer.validated_data['quantity']

        # Edge Case: new quantity exceeds stock
        if new_qty > item.product.stock:
            return Response(
                {'error': f'Only {item.product.stock} item(s) in stock.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        item.quantity = new_qty
        item.save()

        cart = Cart.objects.prefetch_related('items__product').get(id=item.cart.id)
        return Response(CartSerializer(cart).data)

    def delete(self, request, item_id):
        """Remove a specific item from cart."""
        item = self._get_cart_item(item_id, request.user)
        if not item:
            return Response({'error': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

        cart_id = item.cart.id
        item.delete()

        cart = Cart.objects.prefetch_related('items__product').get(id=cart_id)
        return Response(CartSerializer(cart).data)
