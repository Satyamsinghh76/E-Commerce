"""
Seed Script — Populates the database with sample data for testing.

Run with: python seed_data.py
(from the project root, same folder as manage.py)

This creates:
  - 1 superuser (admin / admin123)
  - 1 regular user (anshika / test1234)
  - 4 categories
  - 10 products
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import Category, Product

# ────────────────────────────────────────────────
# 1. Create Users
# ────────────────────────────────────────────────
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Superuser created: admin / admin123")
else:
    print("⏭  Superuser already exists")

if not User.objects.filter(username='anshika').exists():
    User.objects.create_user('anshika', 'anshika@example.com', 'test1234')
    print("✅ User created: anshika / test1234")
else:
    print("⏭  User 'anshika' already exists")

# ────────────────────────────────────────────────
# 2. Create Categories
# ────────────────────────────────────────────────
categories_data = ['T-Shirts', 'Jeans', 'Shoes', 'Dresses']
categories = {}
for name in categories_data:
    cat, created = Category.objects.get_or_create(name=name)
    categories[name] = cat
    if created:
        print(f"✅ Category: {name}")

# ────────────────────────────────────────────────
# 3. Create Products
# ────────────────────────────────────────────────
products_data = [
    {'name': 'Myntra Classic White Tee',     'price': '499.00',  'stock': 50,  'category': 'T-Shirts'},
    {'name': 'Roadster Graphic T-Shirt',     'price': '699.00',  'stock': 30,  'category': 'T-Shirts'},
    {'name': 'H&M Striped Polo',             'price': '899.00',  'stock': 5,   'category': 'T-Shirts'},  # Low stock!
    {'name': 'Levis 511 Slim Fit Jeans',     'price': '2499.00', 'stock': 20,  'category': 'Jeans'},
    {'name': 'Wrangler Stretch Jeans',       'price': '1799.00', 'stock': 15,  'category': 'Jeans'},
    {'name': 'Nike Air Max Sneakers',        'price': '7999.00', 'stock': 10,  'category': 'Shoes'},
    {'name': 'Adidas Ultraboost Running',    'price': '9999.00', 'stock': 8,   'category': 'Shoes'},
    {'name': 'Bata Formal Oxford Shoes',     'price': '1999.00', 'stock': 25,  'category': 'Shoes'},
    {'name': 'Zara Floral Midi Dress',       'price': '3499.00', 'stock': 12,  'category': 'Dresses'},
    {'name': 'ONLY Wrap Maxi Dress',         'price': '2299.00', 'stock': 0,   'category': 'Dresses'},  # Out of stock!
]

for p in products_data:
    product, created = Product.objects.get_or_create(
        name=p['name'],
        defaults={
            'price':    p['price'],
            'stock':    p['stock'],
            'category': categories[p['category']],
            'description': f"Premium quality {p['name']} from top brands.",
        }
    )
    status = "✅" if created else "⏭ "
    print(f"{status} Product: {p['name']} — ₹{p['price']} (Stock: {p['stock']})")

print("\n🎉 Seed complete!")
print("\nQuick Test Commands (Postman / curl):")
print("  POST /api/auth/login/    body: {username: admin, password: admin123}")
print("  GET  /api/products/")
print("  GET  /api/products/?search=nike")
print("  GET  /api/products/low-stock/")
print("  POST /api/cart/          body: {product_id: 1, quantity: 2}")
print("  GET  /api/cart/")
print("  POST /api/orders/        body: {shipping_address: '123 Main St'}")
print("  GET  /api/orders/list/")
