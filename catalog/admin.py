from django.contrib import admin

from .models import Category, Item


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "brand", "price", "currency")
    list_filter = ("category", "currency")
    search_fields = ("name", "source_code", "brand")

# Register your models here.
