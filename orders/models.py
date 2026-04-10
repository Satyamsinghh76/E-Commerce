"""
Order Models — Phase 4

KEY DESIGN DECISIONS:

1. STATUS_CHOICES enforces valid states — no typos possible, DB-validated.

2. price_at_order (SNAPSHOT PATTERN):
   We store the price AT THE TIME OF ORDER, not FK to Product.price.
   WHY: Product prices change. If you bought a shirt for ₹999 and the price 
   changes to ₹1,299 later, your order history must still show ₹999.
   This is called "event sourcing" — record facts as they were, not as they are.

3. product_name (SNAPSHOT):
   Same reason. If product is renamed/deleted, order history still shows 
   what the user actually bought.

4. product FK is SET_NULL (not CASCADE):
   If a product is deleted, the order still exists — just without a product link.
   The product_name + price_at_order snapshots preserve all needed info.

5. ForeignKey user (not OneToOne):
   One user can have MANY orders. OneToOne would only allow one order ever.
"""
from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING',   'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED',   'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price      = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField(default='')
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} — {self.user.username} — {self.status}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    """
    A line item in an order. Contains snapshots of product data at order time.
    """
    order          = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product        = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # SNAPSHOTS — these don't change even if Product changes
    product_name   = models.CharField(max_length=255)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)
    quantity       = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.price_at_order * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product_name} (Order #{self.order.id})"
