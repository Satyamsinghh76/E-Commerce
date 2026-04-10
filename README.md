# Mini E-commerce Backend

A production-style, Myntra-inspired e-commerce system built with Django, Django REST Framework, SQLite/MySQL, and Postman. It includes product catalog APIs, cart operations, order placement, JWT authentication, and a React frontend for demo usage.

![Django](https://img.shields.io/badge/Django-4.x-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-REST%20API-ff1709?logo=django&logoColor=white)
![React](https://img.shields.io/badge/React-Vite-61dafb?logo=react&logoColor=black)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)

## ⭐ Project Highlights

- **API-first ecommerce backend** inspired by real product-company flows.
- **Transactional order service** that prevents partial checkout failures.
- **Snapshot-based order history** so past orders remain accurate even when product data changes.
- **React demo client** connected to live Django APIs for a full end-to-end flow.

## 📌 Overview

This project solves the core backend problem behind modern e-commerce platforms: managing products, user carts, and orders in a clean, scalable, API-first architecture.

In systems like Myntra, Flipkart, or Amazon, the backend must support product discovery, cart updates, order checkout, and historical order tracking while staying fast, consistent, and easy to evolve. This project models those same ideas in a simplified but production-minded way.

## 🏗️ Architecture / System Design

### High-level flow

`User -> React UI / Postman -> Django REST API -> Serializer / View / Service -> Database`

### Core layers

- **Models** define the database schema and relationships.
- **Serializers** validate incoming payloads and convert model instances into JSON.
- **Views** handle HTTP requests, authentication, permissions, and response formatting.
- **Services** contain business logic, especially for order placement and stock updates.
- **Database** stores products, carts, and orders with relational integrity.

### Design philosophy

- Keep views thin.
- Keep business rules in service classes.
- Use snapshots for order history so historical data remains correct even if product data changes later.
- Use transactions for checkout to avoid partial writes.

## ⚙️ Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Authentication:** JWT via SimpleJWT
- **Database:** SQLite for local development, MySQL/PostgreSQL ready for production
- **Frontend:** React + Vite
- **API Testing:** Postman
- **Other:** django-filter, django-cors-headers

## ✨ Features

- **Product Catalog**: Create, view, search, filter, and order products.
- **Category Support**: Organize products into categories.
- **Cart System**: Add items, update quantity, remove items, and clear cart.
- **Order System**: Place orders, view order history, and cancel pending orders.
- **JWT Authentication**: Login and refresh tokens for protected operations.
- **API-First Design**: Clean REST endpoints for frontend or Postman usage.
- **React Demo UI**: A lightweight frontend to interact with the APIs.

## 📂 Folder Structure

```text
Mini E-commerce Backend/
├── ecommerce/          # Project settings, root URLs, WSGI/ASGI config
├── products/           # Product and category models, serializers, views, URLs
├── cart/               # Cart and cart item models, serializers, views, URLs
├── orders/             # Order models, service layer, serializers, views, URLs
├── frontend/           # React + Vite demo client
├── manage.py           # Django management entry point
├── db.sqlite3          # Local SQLite database
├── seed_data.py        # Script to populate sample users, categories, and products
└── README.md           # Project documentation
```

### Important files

- **[ecommerce/settings.py](ecommerce/settings.py)**: Installed apps, REST framework config, JWT config, CORS settings.
- **[ecommerce/urls.py](ecommerce/urls.py)**: Root URL routing and API index endpoint.
- **[products/models.py](products/models.py)**: Product and Category schemas.
- **[products/views.py](products/views.py)**: Product and category APIs.
- **[cart/views.py](cart/views.py)**: Cart add/update/remove logic.
- **[orders/services.py](orders/services.py)**: Transactional order placement and cancellation logic.
- **[frontend/src/App.jsx](frontend/src/App.jsx)**: React demo UI consuming Django APIs.

## 🔌 API Endpoints

Base URL: `http://127.0.0.1:8000`

### Root

- `GET /` - API health/index endpoint

### Auth

- `POST /api/auth/login/` - Obtain access and refresh tokens
- `POST /api/auth/refresh/` - Refresh expired access token

### Products

- `GET /api/products/` - List active products
- `POST /api/products/` - Create product (admin only)
- `GET /api/products/{id}/` - Retrieve product details
- `PATCH /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Soft deactivate product
- `GET /api/products/?search=nike` - Search products
- `GET /api/products/?category=1` - Filter by category
- `GET /api/products/low-stock/` - Low stock report (admin only)

### Categories

- `GET /api/products/categories/` - List categories
- `POST /api/products/categories/` - Create category (admin only)
- `GET /api/products/categories/{id}/` - Category details
- `PATCH /api/products/categories/{id}/` - Update category
- `DELETE /api/products/categories/{id}/` - Delete category

### Cart

- `GET /api/cart/` - View current cart
- `POST /api/cart/` - Add item to cart
- `DELETE /api/cart/` - Clear cart
- `PATCH /api/cart/item/{id}/` - Update quantity
- `DELETE /api/cart/item/{id}/` - Remove cart item

### Orders

- `GET /api/orders/` - List my orders
- `POST /api/orders/` - Place order from cart
- `GET /api/orders/{id}/` - Order detail
- `POST /api/orders/{id}/cancel/` - Cancel a pending order

### Sample request/response

#### Login

**Request**
```json
POST /api/auth/login/
{
  "username": "anshika",
  "password": "test1234"
}
```

**Response**
```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

#### Create cart item

**Request**
```json
POST /api/cart/
{
  "product_id": 1,
  "quantity": 2
}
```

**Response**
```json
{
  "id": 1,
  "items": [
    {
      "id": 1,
      "product": 1,
      "product_name": "Myntra Classic White Tee",
      "product_price": "499.00",
      "quantity": 2,
      "subtotal": "998.00"
    }
  ],
  "total_price": "998.00",
  "total_items": 1,
  "updated_at": "2026-04-10T..."
}
```

#### Place order

**Request**
```json
POST /api/orders/
{
  "shipping_address": "Noida, UP"
}
```

**Response**
```json
{
  "id": 1,
  "status": "PENDING",
  "status_display": "Pending",
  "total_price": "998.00",
  "shipping_address": "Noida, UP",
  "items": [...],
  "created_at": "2026-04-10T...",
  "updated_at": "2026-04-10T..."
}
```

## 🧠 Key Concepts Used

- **REST APIs**: Resource-based endpoints with standard HTTP verbs.
- **ORM**: Django ORM maps Python models to database tables.
- **Layered Architecture**: Views handle HTTP, serializers handle validation, services handle business logic.
- **Transactions**: `transaction.atomic()` ensures checkout consistency.
- **Snapshot Pattern**: Order items store product name and price at purchase time.
- **Relational Modeling**: Foreign keys and one-to-one relationships model product/cart/order flows.

## 🚀 Setup Instructions

### 1) Clone the repository

```bash
git clone https://github.com/Satyamsinghh76/E-Commerce.git
cd E-Commerce
```

### 2) Create and activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3) Install backend dependencies

```bash
pip install django djangorestframework django-filter django-cors-headers djangorestframework-simplejwt
```

### 4) Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5) Seed sample data

```bash
python seed_data.py
```

### 6) Start Django server

```bash
python manage.py runserver
```

### 7) Run the React frontend

```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing

### Postman workflow

1. Call `POST /api/auth/login/` with seeded credentials.
2. Copy the returned `access` token.
3. Add header: `Authorization: Bearer <access-token>`.
4. Test the product, cart, and order endpoints.
5. Verify edge cases like:
   - duplicate cart adds
   - quantity higher than stock
   - canceling non-pending orders
   - order placement from empty cart

### Suggested test accounts

- **Admin**: `admin / admin123`
- **User**: `anshika / test1234`

## 📈 Scalability & Improvements

For a real production system, this design can scale further with:

- **Caching**: Redis for hot product lists and product details.
- **Database optimization**: Add indexes on high-read columns, use read replicas, and move to PostgreSQL/MySQL.
- **Load balancing**: Multiple stateless API instances behind a load balancer.
- **Async processing**: Celery for emails, notifications, and background workflows.
- **Observability**: Centralized logs, metrics, and traces.
- **Service split**: Separate catalog, cart, order, and payment domains when traffic grows.

## ❗ Challenges Faced

- Designing cart logic so duplicate products update quantity instead of creating separate rows.
- Keeping order history correct even if product price or name changes later.
- Ensuring checkout is atomic so stock, order records, and cart cleanup stay consistent.
- Preventing one user from accessing or modifying another user’s cart or orders.
- Balancing a simple codebase with production-style structure and edge-case handling.

## 🔮 Future Enhancements

- Full user registration and profile management
- Payment gateway integration
- Recommendation engine
- Wishlist and saved items
- Pagination and advanced filtering on all list endpoints
- Role-based admin dashboards
- Email notifications for order confirmation and cancellation
- Improved frontend routing and route guards

## 💡 Learnings

- How to model real-world ecommerce flows in Django ORM.
- Why serializers, views, and services should be separated.
- How transactions protect data consistency in checkout systems.
- How snapshot-based order design preserves history.
- How a frontend can interact cleanly with JWT-protected REST APIs.
- How to think about scalability before a project reaches production traffic.

## 👨‍💻 Author

Built by **Satyam Singh** as a Myntra-inspired backend engineering project.

This project was designed to demonstrate backend fundamentals, API design, database modeling, transactional integrity, and frontend-backend integration in a way that is interview-ready and product-company oriented.

---

If you want, I can also add a compact `README` badge section, deployment notes, or a diagram image block for a more polished GitHub presentation.
