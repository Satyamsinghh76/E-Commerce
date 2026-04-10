"""
Order Service — Phase 6 (Clean Architecture)

WHY a service layer?
The OrderService encapsulates ALL order business logic.
The view just calls OrderService.place_order() and handles HTTP response.

BENEFITS:
  - View stays thin (only HTTP concerns)
  - Service is testable without HTTP context
  - Reusable from other places (management commands, Celery tasks, admin actions)
  - Easy to mock in unit tests

TRANSACTION:
@transaction.atomic ensures ALL operations succeed or ALL roll back.
Steps: validate stock → create Order → create OrderItems → decrement stock → clear cart
If step 4 fails, steps 1-3 are automatically rolled back.
"""
from django.db import transaction
from .models import Order, OrderItem
from cart.models import Cart


class OrderService:

    @staticmethod
    @transaction.atomic
    def place_order(user, shipping_address=''):
        """
        Place an order from user's cart.

        Raises:
            Cart.DoesNotExist: if the user has no cart
            ValueError: if cart is empty or stock is insufficient

        Returns:
            Order: the created Order instance
        """
        # Fetch cart with all items and product data in 2 queries (no N+1)
        try:
            cart = Cart.objects.prefetch_related('items__product').get(user=user)
        except Cart.DoesNotExist:
            raise ValueError("You don't have a cart yet.")

        items = list(cart.items.all())

        # Validation 1: Cart must not be empty
        if not items:
            raise ValueError("Your cart is empty.")

        # Validation 2: Check ALL stock before writing ANYTHING
        # Important: validate first, write later — avoids partial failures
        for item in items:
            if item.product.stock < item.quantity:
                raise ValueError(
                    f'Insufficient stock for "{item.product.name}". '
                    f'Available: {item.product.stock}, Requested: {item.quantity}'
                )

        # All validations passed — now create records
        total = sum(item.subtotal for item in items)

        order = Order.objects.create(
            user=user,
            total_price=total,
            shipping_address=shipping_address,
            status='PENDING'
        )

        # Create order items (with snapshots) and decrement stock atomically
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,       # Snapshot
                price_at_order=item.product.price,    # Snapshot
                quantity=item.quantity
            )
            # Decrement stock
            # NOTE: For high-concurrency, use:
            # Product.objects.filter(id=item.product.id).update(stock=F('stock') - item.quantity)
            item.product.stock -= item.quantity
            item.product.save(update_fields=['stock'])  # Only update stock column

        # Clear the cart
        cart.items.all().delete()

        return order

    @staticmethod
    def cancel_order(order, user):
        """
        Cancel a pending order and restore stock.
        Only PENDING orders can be cancelled.
        """
        if order.user != user:
            raise PermissionError("You can only cancel your own orders.")

        if order.status != 'PENDING':
            raise ValueError(f"Cannot cancel an order with status '{order.status}'.")

        # Restore stock for each item
        for item in order.items.select_related('product').all():
            if item.product:
                item.product.stock += item.quantity
                item.product.save(update_fields=['stock'])

        order.status = 'CANCELLED'
        order.save(update_fields=['status'])
        return order
