import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from catalog.models import Category, Item


class Command(BaseCommand):
    help = "Import categories and shopping items from the offline CSV datasets."

    def handle(self, *args, **options):
        data_dir = Path(__file__).resolve().parents[3] / "data"
        categories_path = data_dir / "categories.csv"
        items_path = data_dir / "shopping_items.csv"

        categories_created = 0
        categories_updated = 0
        imported = 0
        updated = 0

        with categories_path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
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

        with items_path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                category = Category.objects.get(code=row["category_code"])
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

        self.stdout.write(
            self.style.SUCCESS(
                "Import complete: "
                f"{categories_created} categories created, "
                f"{categories_updated} categories updated, "
                f"{imported} items created, "
                f"{updated} items updated."
            )
        )
