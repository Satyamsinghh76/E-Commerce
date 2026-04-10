"""
Order Views — Phase 4

THIN VIEWS: All business logic lives in OrderService.
Views only handle:
  - Request parsing
  - Calling the service
  - HTTP status codes and response formatting
  - Error translation (ValueError → 400, PermissionError → 403)

Endpoints:
  POST   /api/orders/      → Place order from cart
  GET    /api/orders/      → List my orders (newest first)
  GET    /api/orders/{id}/ → Get specific order
  POST   /api/orders/{id}/cancel/ → Cancel a pending order
"""
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer, PlaceOrderSerializer
from .services import OrderService


class OrderListCreateView(APIView):
    """GET /api/orders/ (list) and POST /api/orders/ (place order)."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Order.objects.filter(user=request.user).prefetch_related('items__product')
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = OrderService.place_order(
                user=request.user,
                shipping_address=serializer.validated_data.get('shipping_address', '')
            )
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            # Business rule violations (empty cart, out of stock)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Unexpected errors — log in production, return generic message
            return Response(
                {'error': 'Failed to place order. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderDetailView(generics.RetrieveAPIView):
    """GET /api/orders/{id}/ — Get specific order details."""
    serializer_class   = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related('items__product')


class CancelOrderView(APIView):
    """POST /api/orders/{id}/cancel/ — Cancel a pending order."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            order = OrderService.cancel_order(order, user=request.user)
            return Response(OrderSerializer(order).data)
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
