"""
Order Serializers — Phase 4
"""
from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model  = OrderItem
        fields = ['id', 'product', 'product_name', 'price_at_order', 'quantity', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items       = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model  = Order
        fields = [
            'id', 'status', 'status_display', 'total_price',
            'shipping_address', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'total_price', 'created_at', 'updated_at']


class PlaceOrderSerializer(serializers.Serializer):
    """Input serializer — only shipping address needed. Cart data is fetched server-side."""
    shipping_address = serializers.CharField(required=False, default='', allow_blank=True)
