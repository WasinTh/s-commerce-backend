# Simple Commerce Backend

Django REST API for a small e-commerce store: product catalog, member auth, shopping cart, and checkout with payment slip upload. Also exposes an MCP endpoint so AI agents can query catalog/sale data and run checkout.

## Stack

- **Python** ≥ 3.14, **Django** ≥ 6.1
- **Django REST Framework** + **SimpleJWT**
- **django-filter**, **drf-spectacular** (OpenAPI / Swagger)
- **django-cors-headers**, **Pillow**
- **django-mcp-server** (MCP tools)
- **SQLite** (default)
- Package manager: **[uv](https://github.com/astral-sh/uv)**

## Apps

| App | Role |
|-----|------|
| `catalog` | Categories & products (list, detail, filters, pagination) |
| `shop` | Member register/login, banners |
| `sale` | Cart, cart items, checkout / payment slip |

## Quick start

```bash
# Install dependencies (creates .venv)
uv sync

# Activate the virtualenv (optional if you use `uv run`)
source .venv/bin/activate

# Apply migrations
uv run python manage.py migrate

# Create an admin user (optional)
uv run python manage.py createsuperuser

# Run the server
uv run python manage.py runserver
```

API base: `http://127.0.0.1:8000/`

### Tests

```bash
uv sync --group dev
uv run pytest
```

## Auth

Most endpoints require a JWT access token (`Authorization: Bearer <token>`).

- **Register** — `POST /api/shop/register/`  
  Body: `email`, `password`, `first_name`, `last_name`, `address`
- **Login** — `POST /api/shop/login/`  
  Body: `email`, `password`  
  Returns `{ "token": "...", "user": { ... } }`

Register and login are public. Default DRF permission is authenticated.

## Main endpoints

### Shop — `/api/shop/`

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/register/` | Create member (+ cart) |
| `POST` | `/login/` | JWT login |
| `GET` | `/banner/` | List banners |

### Catalog — `/api/catalog/`

| Method | Path | Description |
|--------|------|-------------|
| `GET` / `POST` | `/category/` | List / create categories |
| `GET` | `/product/` | Paginated products (`page`, `page_size`) |
| `GET` | `/product-detail/<id>/` | Product detail |

Product filters (query params): `name` (icontains), `cheap` (`true`/`false` — price ≤ / > 10,000).

### Sale — `/api/sale/`

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/add-cart-item/` | Add item (`product`, `quantity`) |
| `GET` | `/cart-detail/` | Current member’s cart |
| `POST` | `/submit-payment/` | Checkout (`email`, `shipping_address`, `slip_image`) |

Checkout clears cart items and creates an `Order` with `OrderItem`s (status defaults to `pending`).

## Docs & admin

| URL | Description |
|-----|-------------|
| `/api/swagger/` | Swagger UI |
| `/api/redoc/` | ReDoc |
| `/api/schema/` | OpenAPI schema |
| `/api/admin/` | Django admin |

Media is served under `/api-media/` in development.

## MCP

MCP is mounted via `mcp_server` at **`/api/mcp/`** (JWT auth). Toolsets include:

- **Catalog**: query `Category`, `Product`
- **Sale**: query `Cart`, `CartItem`, `Order`, `OrderItem`; tool `do_checkout_cart`

## Project layout

```
simple_commerce_backend/   # settings, root URLs
catalog/                   # products & categories
shop/                      # members & banners
sale/                      # cart & orders
media/                     # uploaded images (gitignored)
manage.py
pyproject.toml
```

## Notes

- Default DB is `db.sqlite3` (gitignored). Time zone: `Asia/Bangkok`.
- `CORS_ALLOW_ALL_ORIGINS = True` and a long JWT lifetime are for local/dev use — tighten these for production.
- Dev extras (`pytest-django`, `factory-boy`, `django-silk`) live under the `dev` dependency group.
