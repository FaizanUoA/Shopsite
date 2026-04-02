# Shopsite

A database-driven Django grocery catalogue built for the Enterprise Software Development assignment (Aberdeen University, Semester 2).

## Features

- **Two related tables** — `Category` and `Item` linked with a foreign key
- **500 imported items** across 6 categories (Dry Goods, Drinks, Snacks, Bakery, Frozen, Household)
- **Search** items by name
- **Pagination** — 10 items per page with Previous / Next navigation
- **Item detail pages** showing full product info and linked category
- **User authentication** — register, log in, log out (Django built-in auth)
- **Favourites** — logged-in users can save/remove items with a ★ star toggle; guest users can browse without an account

## Project structure

```
catalog/
  models.py          – Category, Item, Favourite models
  views.py           – item_list, item_detail, register_view, favourite_list, toggle_favourite
  urls.py            – app-level URL patterns
  templates/
    catalog/
      item_list.html     – paginated list with search and favourite stars
      item_detail.html   – product detail with add/remove favourite button
      register.html      – registration form
      favourites.html    – user's saved favourites
    registration/
      login.html         – login form (used by Django's built-in LoginView)
  management/commands/
    import_items.py    – imports categories.csv and shopping_items.csv
data/
  categories.csv       – 6 categories
  shopping_items.csv   – 500 items (I001–I500)
shopsite/
  settings.py          – project settings
  urls.py              – project-level URL routing
```

## Setup and run

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py import_items
python manage.py createsuperuser   # optional — for admin access
python manage.py test
python manage.py runserver
```

## URLs

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Item list (paginated, searchable) |
| `http://127.0.0.1:8000/items/<id>/` | Item detail page |
| `http://127.0.0.1:8000/register/` | Create a new account |
| `http://127.0.0.1:8000/accounts/login/` | Log in |
| `http://127.0.0.1:8000/accounts/logout/` | Log out (POST only) |
| `http://127.0.0.1:8000/favourites/` | My Favourites (login required) |
| `http://127.0.0.1:8000/admin/` | Django admin panel |

## How favourites work

1. Register or log in
2. On the item list, click ☆ next to any item to save it — the star turns ★
3. Click ★ again to remove it
4. Visit **My Favourites** in the nav bar to see all saved items
5. Guests can browse freely without an account
