from django.core.management.base import BaseCommand
from django.utils.text import slugify

from shop.models import Category, Product


PRODUCTS = [
    ("Desk essentials", "desk-essentials", "A warm, useful edit for calmer workdays.", "34.00", 18, True, "Workspace"),
    ("Cloud mug", "cloud-mug", "A stoneware mug with a soft matte glaze and generous handle.", "22.00", 24, True, "Home"),
    ("Field notes set", "field-notes-set", "Three pocket notebooks for ideas, lists, and little observations.", "16.00", 40, False, "Workspace"),
    ("Everyday tote", "everyday-tote", "A durable cotton canvas carryall for errands and weekends away.", "28.00", 21, True, "Travel"),
    ("Cedar candle", "cedar-candle", "Cedarwood, amber, and a hint of smoke in a reusable glass jar.", "30.00", 12, False, "Home"),
    ("Weekend cap", "weekend-cap", "A low-profile cotton cap with an adjustable brass clasp.", "26.00", 16, False, "Apparel"),
    ("Linen throw", "linen-throw", "A light, breathable layer for reading corners and slow Sundays.", "74.00", 8, True, "Home"),
    ("Trail bottle", "trail-bottle", "Double-wall stainless steel bottle that keeps drinks cool for hours.", "42.00", 14, False, "Travel"),
]


class Command(BaseCommand):
    help = "Create the demo catalog for Northstar Market."

    def handle(self, *args, **options):
        for name, slug, description, price, stock, featured, category_name in PRODUCTS:
            category, _ = Category.objects.get_or_create(slug=slugify(category_name), defaults={"name": category_name})
            Product.objects.update_or_create(
                slug=slug,
                defaults={
                    "category": category,
                    "name": name,
                    "description": description,
                    "price": price,
                    "stock": stock,
                    "featured": featured,
                },
            )
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(PRODUCTS)} products."))
