"""
Product Serializers — Phase 2

WHY serializers?
A serializer is the translator between:
  - HTTP world: raw JSON strings (what Postman sends/receives)
  - Python world: Django model instances (what our views work with)

Flow IN  (request): JSON → serializer.is_valid() → validated_data → .save() → DB
Flow OUT (response): DB object → serializer(obj).data → JSON response

ADVANCED: We use 'source' to expose category_name alongside category_id.
This is called a "nested field" — common in real APIs.
"""
from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    # Read-only nested field — shows category name without a separate API call
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model  = Product
        fields = [
            'id', 'name', 'description', 'price',
            'stock', 'category', 'category_name',
            'image_url', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'category_name']

    # Field-level validation — runs automatically during is_valid()
    def validate_price(self, value):
        """Price must be positive — no free or negative-priced products."""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_stock(self, value):
        """Stock can't be negative — even though DB enforces this, we validate early."""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value
