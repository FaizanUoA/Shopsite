# This file controls how Category and Item appear in Django's admin interface.
# Having the admin set up properly means we can browse and edit the database
# through a nice UI without needing DB tools or the shell.

from django.contrib import admin

from .models import Category, Item


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Show name and code in the list so we can quickly see all categories at a glance
    list_display = ("name", "code")
    # Allow searching by name or code in the admin search bar
    search_fields = ("name", "code")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    # The most useful columns for quickly scanning a big list of items
    list_display = ("name", "category", "brand", "price", "currency")
    # Sidebar filters make it easy to narrow down items by category or currency
    list_filter = ("category", "currency")
    # source_code is included so we can look up an item by its original dataset ID
    search_fields = ("name", "source_code", "brand")
