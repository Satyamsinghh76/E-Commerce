"""
Root URL Configuration — ecommerce project
All app URLs are namespaced and included here.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def api_root(request):
    return JsonResponse({
        'message': 'Mini E-commerce Backend is running.',
        'endpoints': {
            'admin': '/admin/',
            'login': '/api/auth/login/',
            'refresh': '/api/auth/refresh/',
            'products': '/api/products/',
            'cart': '/api/cart/',
            'orders': '/api/orders/',
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    # Admin panel
    path('admin/', admin.site.urls),

    # JWT Auth endpoints
    # POST /api/auth/login/   → get access + refresh tokens
    # POST /api/auth/refresh/ → get new access token using refresh token
    path('api/auth/login/',   TokenObtainPairView.as_view(),  name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(),     name='token_refresh'),

    # App-level URL configurations
    path('api/products/', include('products.urls')),
    path('api/cart/',     include('cart.urls')),
    path('api/orders/',   include('orders.urls')),
]
