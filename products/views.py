"""
Product Views — Phase 2

WHY ModelViewSet?
One class → 5 endpoints auto-generated:
  GET    /api/products/        → list()
  POST   /api/products/        → create()
  GET    /api/products/{id}/   → retrieve()
  PUT    /api/products/{id}/   → update()
  PATCH  /api/products/{id}/   → partial_update()
  DELETE /api/products/{id}/   → destroy()

Search: ?search=blue+jeans
Filter: ?category=1
Order:  ?ordering=price or ?ordering=-price (descending)

select_related('category') → JOIN query, avoids N+1 for category name
"""
from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for products.
    Public: GET (list, retrieve)
    Admin only: POST, PUT, PATCH, DELETE
    """
    queryset         = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields    = ['name', 'description']        # ?search=query
    ordering_fields  = ['price', 'created_at', 'name']  # ?ordering=price
    ordering         = ['-created_at']

    def get_permissions(self):
        """
        WHY: Product creation/update should only be for admins.
        Regular users can read (GET) but not write (POST/PUT/DELETE).
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(detail=False, methods=['get'], url_path='low-stock', permission_classes=[permissions.IsAdminUser])
    def low_stock(self, request):
        """
        Custom action: GET /api/products/low-stock/
        Shows products with stock < 10 — useful for inventory alerts.
        'detail=False' means it's a list-level action (not product-specific)
        """
        low = self.get_queryset().filter(stock__lt=10)
        serializer = self.get_serializer(low, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='deactivate', permission_classes=[permissions.IsAdminUser])
    def deactivate(self, request, pk=None):
        """
        Custom action: POST /api/products/{id}/deactivate/
        Soft-deletes a product — sets is_active=False instead of deleting.
        'detail=True' means it acts on a specific product by ID.
        """
        product = self.get_object()
        product.is_active = False
        product.save()
        return Response({'message': f'"{product.name}" has been deactivated.'})


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD for product categories."""
    queryset         = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
