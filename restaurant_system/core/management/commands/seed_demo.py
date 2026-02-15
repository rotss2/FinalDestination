from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from menu.models import Category, MenuItem
from reservations.models import Table, Announcement, Reservation
import random

User = get_user_model()

class Command(BaseCommand):
    help = "Seed demo data for TableFlow"

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_superuser("admin", "admin@example.com", "adminpass123")
            self.stdout.write(self.style.SUCCESS("Created admin: admin / adminpass123"))
        else:
            admin = User.objects.get(username="admin")

        if not User.objects.filter(username="customer").exists():
            customer = User.objects.create_user("customer", "customer@example.com", "customerpass123")
            self.stdout.write(self.style.SUCCESS("Created customer: customer / customerpass123"))
        else:
            customer = User.objects.get(username="customer")

        # tables
        if Table.objects.count() == 0:
            for i, cap in enumerate([2,2,4,4,6,8], start=1):
                Table.objects.create(number=str(i), capacity=cap, table_type="indoor" if i%2 else "outdoor")
            self.stdout.write(self.style.SUCCESS("Created demo tables."))

        # categories + items
        demo = {
            "Starters": [("Garlic Bread", "Toasted, buttery, and addictive.", 120),
                        ("Caesar Salad", "Crisp greens with creamy dressing.", 180)],
            "Mains": [("Grilled Chicken", "Served with seasonal vegetables.", 320),
                      ("Beef Burger", "Juicy patty with house sauce.", 280)],
            "Desserts": [("Chocolate Cake", "Rich and moist.", 160),
                         ("Fruit Parfait", "Light, fresh, and sweet.", 150)]
        }
        for cat_name, items in demo.items():
            cat, _ = Category.objects.get_or_create(name=cat_name, slug=slugify(cat_name))
            for name, desc, price in items:
                MenuItem.objects.get_or_create(category=cat, name=name, defaults={"description": desc, "price": price})

        # announcement
        Announcement.objects.get_or_create(
            title="Welcome to TableFlow",
            defaults={"message": "Book ahead, chat with support, and watch this board for updates.", "priority": 1, "is_active": True}
        )

        # sample reservation
        if Reservation.objects.filter(user=customer).count() == 0:
            table = Table.objects.filter(is_active=True).order_by("capacity").first()
            start = timezone.now() + timezone.timedelta(days=1, hours=2)
            Reservation.objects.create(user=customer, table=table, start_dt=start, guests=2, status="confirmed")
            self.stdout.write(self.style.SUCCESS("Created a sample reservation."))

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))

