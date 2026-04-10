"""
Cart Models — Phase 3

SCHEMA DESIGN:
  User (1) ──── Cart (1) ──── CartItem (M) ──── Product

WHY OneToOne for Cart?
Each user has exactly one cart. OneToOneField enforces this at DB level.

WHY unique_together on CartItem?
Same product can't appear twice in the same cart.
If user adds the same product again → we UPDATE quantity, not INSERT a new row.

WHY subtotal as @property?
We compute it on-the-fly from price × quantity.
Never store computed values in DB — they get out of sync.
"""
from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total_price(self):
        """Sum of all item subtotals — computed dynamically."""
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        """Count of cart items (not total quantity)."""
        return self.items.count()


class CartItem(models.Model):
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        # CRITICAL: Enforces no duplicate products per cart at DB level
        unique_together = ['cart', 'product']

    @property
    def subtotal(self):
        """
        Uses CURRENT product price. 
        Note: OrderItem uses price_at_order (snapshot) — cart items use live price.
        This is intentional: cart shows current price, order locks it in.
        """
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in {self.cart}"
