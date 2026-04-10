"""
Product URLs — Phase 2

Router auto-generates clean URLs:
  products/          ← ProductViewSet  (list + create)
  products/{id}/     ← ProductViewSet  (retrieve + update + delete)
  products/low-stock/ ← custom action
  categories/        ← CategoryViewSet
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
