# Automated tests for the catalog app.
# Run with: python manage.py test catalog
#
# The test data is set up once per class (setUpTestData) rather than before
# every single test, which makes the suite run significantly faster because
# the database records are only created once and rolled back after the class
# rather than being created and destroyed for each individual test.

from django.test import TestCase
from django.urls import reverse

from .models import Category, Item


class CatalogViewTests(TestCase):
    # Creates a small but realistic set of test data: three categories and
    # one item in each. All the other test classes in this file inherit from
    # or reuse this data through subclassing.
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
        # Checks that the homepage returns 200, uses the right template, and
        # actually shows items — a basic smoke test to catch any wiring problems
        response = self.client.get(reverse("item_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/item_list.html")
        self.assertContains(response, "Basmati Rice")
        self.assertContains(response, "Apple Juice")


class ItemSearchTests(CatalogViewTests):
    # All search tests reuse the data from CatalogViewTests by inheriting it,
    # so we don't have to set up the same items twice.

    def test_search_rice_returns_rice_item(self):
        # "rice" should match "Basmati Rice" but nothing else in the test data
        response = self.client.get(reverse("item_list"), {"search": "rice"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Basmati Rice")
        self.assertNotContains(response, "Apple Juice")
        self.assertNotContains(response, "Dark Chocolate")

    def test_search_juice_returns_juice_item(self):
        # Verifies that the search is item-specific, not returning everything
        response = self.client.get(reverse("item_list"), {"search": "juice"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Apple Juice")
        self.assertNotContains(response, "Basmati Rice")
        self.assertNotContains(response, "Dark Chocolate")

    def test_search_with_no_match_returns_no_items(self):
        # When there's no match, the template should show an empty-state message
        # rather than a blank page with no explanation
        response = self.client.get(reverse("item_list"), {"search": "coffee"})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Basmati Rice")
        self.assertNotContains(response, "Apple Juice")
        self.assertNotContains(response, "Dark Chocolate")
        self.assertContains(response, "No items have been imported yet.")


class ItemRelationshipAndPaginationTests(TestCase):
    # Uses a fresh dataset: 30 items in one category.
    # 30 items is enough to produce 3 pages at 10-per-page and test that
    # the second page doesn't include items from the first.
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
        # Makes sure the detail view correctly joins the Category table so
        # the category name and description appear on the item detail page
        item = Item.objects.get(source_code="P001")

        response = self.client.get(reverse("item_detail", args=[item.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Category A")
        self.assertContains(response, "Used for pagination and relationship tests.")

    def test_list_page_is_paginated_to_ten_items(self):
        # Confirms that page 1 only contains 10 items even though 30 exist,
        # and that the paginator knows about all 30
        response = self.client.get(reverse("item_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["items"]), 10)
        self.assertEqual(response.context["page_obj"].paginator.count, 30)
        self.assertContains(response, "Page 1 of 3")

    def test_second_page_shows_next_set_of_items(self):
        # Items are ordered by price (ascending), so page 2 should start from
        # item 11 and not contain anything from page 1
        response = self.client.get(reverse("item_list"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Item 11")
        self.assertNotContains(response, "Sample Item 01")
