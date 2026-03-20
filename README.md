# Assignment 1 Helper

This helper project extends the Lecture 2 Django practical into a slightly richer data model.

It includes:

- two linked tables: `Category` and `Item`
- an offline dataset split across two CSV files
- 30 imported items
- pagination with a maximum of 10 items per page
- item detail pages that show related category information
- the same search-by-name feature from the earlier practical

## Main pieces

- `catalog/models.py`: `Category` and `Item` models linked with a foreign key
- `data/categories.csv`: category dataset
- `data/shopping_items.csv`: item dataset
- `catalog/management/commands/import_items.py`: imports both datasets
- `catalog/views.py`: list/detail views with search and pagination
- `catalog/templates/catalog/item_list.html`: paginated list page
- `catalog/templates/catalog/item_detail.html`: detail page showing the linked category

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py import_items
python manage.py test
python manage.py runserver
```

Then open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/?page=2`
- `http://127.0.0.1:8000/items/1/`

## What to look at

- the list page only shows 10 items at a time
- the `Previous` and `Next` links move between pages
- every item belongs to a category
- the item detail page shows category information from the linked table
