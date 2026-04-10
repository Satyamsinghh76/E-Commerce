"""
Orders URLs — Phase 4

Endpoints:
  POST   /api/orders/              → Place order
  GET    /api/orders/              → List my orders
  GET    /api/orders/{id}/         → Order detail
  POST   /api/orders/{id}/cancel/  → Cancel order
"""
from django.urls import path
from .views import OrderListCreateView, OrderDetailView, CancelOrderView

urlpatterns = [
  path('', OrderListCreateView.as_view(), name='order-list-create'),
  path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/cancel/', CancelOrderView.as_view(), name='cancel-order'),
]
