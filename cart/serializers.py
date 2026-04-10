"""
Cart Serializers — Phase 3

We use TWO different serializers for reading vs writing:
  - CartSerializer / CartItemSerializer : for GET responses (rich data)
  - AddToCartSerializer                 : for POST body validation (input only)

WHY separate input serializer?
The user sends: { "product_id": 5, "quantity": 2 }
But the response needs: product name, price, subtotal, total...
Mixing input/output in one serializer leads to messy code.
"""
from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    # Extra read-only fields sourced from related product
    product_name  = serializers.CharField(source='product.name',  read_only=True)
    product_price = serializers.DecimalField(
        source='product.price', max_digits=10, decimal_places=2, read_only=True
    )
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model  = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'subtotal']


class CartSerializer(serializers.ModelSerializer):
    items       = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model  = Cart
        fields = ['id', 'items', 'total_price', 'total_items', 'updated_at']


class AddToCartSerializer(serializers.Serializer):
    """
    Input-only serializer for POST /api/cart/
    Validates product exists and quantity is reasonable.
    """
    product_id = serializers.IntegerField()
    quantity   = serializers.IntegerField(min_value=1, max_value=100)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Product not found or has been removed.")
        return value


class UpdateCartItemSerializer(serializers.Serializer):
    """Input serializer for PATCH /api/cart/item/{id}/"""
    quantity = serializers.IntegerField(min_value=1, max_value=100)
