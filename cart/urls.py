"""
Cart URLs — Phase 3

Endpoints:
  GET    /api/cart/             → View cart
  POST   /api/cart/             → Add item
  DELETE /api/cart/             → Clear cart
  PATCH  /api/cart/item/{id}/   → Update item quantity
  DELETE /api/cart/item/{id}/   → Remove item
"""
from django.urls import path
from .views import CartView, CartItemView

urlpatterns = [
    path('',             CartView.as_view(),            name='cart'),
    path('item/<int:item_id>/', CartItemView.as_view(), name='cart-item'),
]
