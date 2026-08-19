# Northstar Market

A small, database-backed e-commerce site built with Django, HTML, CSS, and vanilla JavaScript.

## Included

- Product listing with category filters and search
- Product detail pages with stock-aware add-to-bag controls
- Session-based shopping cart
- User registration, login, logout, and order history
- Authenticated checkout with shipping details
- Transactional order creation that decrements stock safely
- Django admin for products, categories, and order status management
- SQLite database for local development

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_products
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. The admin is at `http://127.0.0.1:8000/admin/`.

The project uses SQLite by default. Set a production `SECRET_KEY`, turn off `DEBUG`, configure `ALLOWED_HOSTS`, and use a production database before deploying.
