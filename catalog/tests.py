from django.test import TestCase
from django.urls import reverse

from .models import Category, Item


class CatalogViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        dry_goods = Category.objects.create(
            code="DRY",
            name="Dry Goods",
            description="Long-lasting pantry staples.",
        )
        drinks = Category.objects.create(
            code="DRK",
            name="Drinks",
            description="Beverages and juices.",
        )
        snacks = Category.objects.create(
            code="SNK",
            name="Snacks",
            description="Quick snacks and sweet treats.",
        )

        Item.objects.create(
            source_code="T001",
            name="Basmati Rice",
            category=dry_goods,
            brand="Test Brand",
            price=2.40,
            currency="GBP",
            size="1 kg",
            description="Long-grain rice.",
        )
        Item.objects.create(
            source_code="T002",
            name="Apple Juice",
            category=drinks,
            brand="Test Brand",
            price=1.75,
            currency="GBP",
            size="1 L",
            description="Pressed apple juice.",
        )
        Item.objects.create(
            source_code="T003",
            name="Dark Chocolate",
            category=snacks,
            brand="Test Brand",
            price=1.60,
            currency="GBP",
            size="100 g",
            description="Dark chocolate bar.",
        )

    def test_item_list_page_loads_and_uses_template(self):
        response = self.client.get(reverse("item_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/item_list.html")
        self.assertContains(response, "Basmati Rice")
        self.assertContains(response, "Apple Juice")


class ItemSearchTests(CatalogViewTests):
    def test_search_rice_returns_rice_item(self):
        response = self.client.get(reverse("item_list"), {"search": "rice"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Basmati Rice")
        self.assertNotContains(response, "Apple Juice")
        self.assertNotContains(response, "Dark Chocolate")

    def test_search_juice_returns_juice_item(self):
        response = self.client.get(reverse("item_list"), {"search": "juice"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Apple Juice")
        self.assertNotContains(response, "Basmati Rice")
        self.assertNotContains(response, "Dark Chocolate")

    def test_search_with_no_match_returns_no_items(self):
        response = self.client.get(reverse("item_list"), {"search": "coffee"})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Basmati Rice")
        self.assertNotContains(response, "Apple Juice")
        self.assertNotContains(response, "Dark Chocolate")
        self.assertContains(response, "No items have been imported yet.")


class ItemRelationshipAndPaginationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            code="CAT",
            name="Category A",
            description="Used for pagination and relationship tests.",
        )

        for index in range(1, 31):
            Item.objects.create(
                source_code=f"P{index:03d}",
                name=f"Sample Item {index:02d}",
                category=category,
                brand="Test Brand",
                price=f"{index}.00",
                currency="GBP",
                size="1 unit",
                description=f"Description for item {index}.",
            )

    def test_detail_page_shows_related_category(self):
        item = Item.objects.get(source_code="P001")

        response = self.client.get(reverse("item_detail", args=[item.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Category A")
        self.assertContains(response, "Used for pagination and relationship tests.")

    def test_list_page_is_paginated_to_ten_items(self):
        response = self.client.get(reverse("item_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["items"]), 10)
        self.assertEqual(response.context["page_obj"].paginator.count, 30)
        self.assertContains(response, "Page 1 of 3")

    def test_second_page_shows_next_set_of_items(self):
        response = self.client.get(reverse("item_list"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Item 11")
        self.assertNotContains(response, "Sample Item 01")
