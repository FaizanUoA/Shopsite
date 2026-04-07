# Custom management command: python manage.py import_items
# Run this once (or again after changing the CSVs) to load the dataset into the database.
# Using update_or_create means re-running the command is always safe -- it won't
# create duplicate records, it just updates anything that changed in the CSV.

import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from catalog.models import Category, Item


class Command(BaseCommand):
    help = "Import categories and shopping items from the offline CSV datasets."

    def handle(self, *args, **options):
        # Build the path to the data/ folder relative to this file so the command
        # works no matter where the project is cloned on disk
        data_dir = Path(__file__).resolve().parents[3] / "data"
        categories_path = data_dir / "categories.csv"
        items_path = data_dir / "shopping_items.csv"

        # Keep separate counters so the summary message is actually informative
        categories_created = 0
        categories_updated = 0
        imported = 0
        updated = 0

        # --- Import categories first ---
        # Categories must exist before items because items have a FK to Category
        with categories_path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Look up by code; if it exists, update name/description instead of inserting a duplicate
                _, created = Category.objects.update_or_create(
                    code=row["code"],
                    defaults={
                        "name": row["name"],
                        "description": row["description"],
                    },
                )
                if created:
                    categories_created += 1
                else:
                    categories_updated += 1

        # --- Import items ---
        with items_path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Resolve the category FK using the code column in the CSV
                category = Category.objects.get(code=row["category_code"])
                # source_code is the unique ID from the original dataset; it's used
                # as the lookup key so reruns don't create duplicates
                _, created = Item.objects.update_or_create(
                    source_code=row["source_code"],
                    defaults={
                        "name": row["name"],
                        "category": category,
                        "brand": row["brand"],
                        "price": row["price"],
                        "currency": row["currency"],
                        "size": row["size"],
                        "description": row["description"],
                    },
                )
                if created:
                    imported += 1
                else:
                    updated += 1

        # Print a coloured success summary to the terminal
        self.stdout.write(
            self.style.SUCCESS(
                "Import complete: "
                f"{categories_created} categories created, "
                f"{categories_updated} categories updated, "
                f"{imported} items created, "
                f"{updated} items updated."
            )
        )
