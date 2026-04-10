"""
Product Models — Phase 2

WHY two models?
- Category keeps products organized (Shirts, Shoes, Electronics...)
- Product stores all item details
- ForeignKey creates a "many products → one category" relationship

DESIGN NOTES:
- We never hard-delete products (is_active=False soft delete)
- Decimal for price (not Float — float has precision errors with money!)
- PositiveIntegerField for stock — DB rejects negative values automatically
- Indexes on 'name' and 'price' for faster search/filter queries
"""
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name        = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, default='')
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField(default=0)
    category    = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # If category deleted, product stays (null category)
        null=True,
        blank=True,
        related_name='products'
    )
    image_url   = models.URLField(blank=True, default='')
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)  # Set once on creation
    updated_at  = models.DateTimeField(auto_now=True)      # Updated on every save

    def __str__(self):
        return f"{self.name} (₹{self.price})"

    class Meta:
        ordering = ['-created_at']  # Newest products first by default
        indexes = [
            models.Index(fields=['name']),   # Fast name filter/search
            models.Index(fields=['price']),  # Fast price filter/sort
        ]
