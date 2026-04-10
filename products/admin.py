"""
Product Admin — registers models in Django's auto-generated admin panel.
Visit http://127.0.0.1:8000/admin/ to manage products with a nice GUI.
"""
from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'stock', 'is_active', 'created_at']
    list_filter  = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_active']
    ordering = ['-created_at']
