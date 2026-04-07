from django.conf import settings
from django.db import models

# This file defines the three database tables (models) that power the Shopsite app.
# Category and Item have a one-to-many relationship — a single category can contain
# many items, but each item belongs to exactly one category.
# Favourite is a join table that connects a logged-in user to items they've saved,
# so it sits between Django's built-in User model and our Item model.


class Category(models.Model):
    # Short identifier that matches the category_code column in the CSV data,
    # e.g. "DRY", "FRZ", "DRK". Kept unique so re-importing is safe.
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        # Sort categories alphabetically in all queries by default
        ordering = ["name"]
        # Django would auto-generate "categorys" without this fix
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Item(models.Model):
    # source_code comes straight from the dataset and acts as a stable identifier,
    # which makes it easy to re-run the import command without creating duplicates.
    source_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    # Deleting a category removes all its items too — CASCADE keeps the DB consistent.
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="items"
    )
    brand = models.CharField(max_length=100, blank=True)
    # DecimalField is used instead of FloatField here to avoid floating-point
    # rounding errors when dealing with prices.
    price = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=10, default="GBP")
    size = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        # Items appear in alphabetical order unless the view overrides this
        ordering = ["name"]

    def __str__(self):
        return self.name


class Favourite(models.Model):
    # Using settings.AUTH_USER_MODEL instead of importing User directly keeps
    # this model compatible if the project ever swaps to a custom user model.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favourites"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="favourited_by")
    # auto_now_add stamps the exact moment a favourite was saved — useful for
    # ordering the list with the most recently added item at the top.
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents the same user from adding the same item twice
        unique_together = ("user", "item")
        # Show the most recently favourited item first in the list view
        ordering = ["-added"]

    def __str__(self):
        return f"{self.user} — {self.item}"