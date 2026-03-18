import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from bikes.models import Bike

User = get_user_model()

BIKES_DATA = [
    {
        "title": "Yamaha R1 in excellent condition",
        "brand": "Yamaha", "model": "YZF-R1", "year": 2021,
        "engine_cc": 998, "price": Decimal('14500.00'), "mileage": 8500,
        "fuel_type": "Petrol", "condition": "Excellent",
        "city": "Los Angeles", "state": "CA",
    },
    {
        "title": "Honda CBR600RR - Track Ready",
        "brand": "Honda", "model": "CBR600RR", "year": 2019,
        "engine_cc": 599, "price": Decimal('9500.00'), "mileage": 12000,
        "fuel_type": "Petrol", "condition": "Good",
        "city": "Chicago", "state": "IL",
    },
    {
        "title": "Suzuki GSX-R1000 - Low Mileage",
        "brand": "Suzuki", "model": "GSX-R1000", "year": 2020,
        "engine_cc": 999, "price": Decimal('12500.00'), "mileage": 5000,
        "fuel_type": "Petrol", "condition": "Excellent",
        "city": "New York", "state": "NY",
    },
    {
        "title": "Kawasaki Ninja 400 - Beginner Friendly",
        "brand": "Kawasaki", "model": "Ninja 400", "year": 2022,
        "engine_cc": 399, "price": Decimal('5200.00'), "mileage": 3000,
        "fuel_type": "Petrol", "condition": "Excellent",
        "city": "Houston", "state": "TX",
    },
    {
        "title": "Ducati Panigale V2 - Needs TLC",
        "brand": "Ducati", "model": "Panigale V2", "year": 2021,
        "engine_cc": 955, "price": Decimal('13000.00'), "mileage": 15000,
        "fuel_type": "Petrol", "condition": "Fair",
        "city": "Miami", "state": "FL",
    },
    {
        "title": "BMW S1000RR M Package",
        "brand": "BMW", "model": "S1000RR", "year": 2023,
        "engine_cc": 999, "price": Decimal('22500.00'), "mileage": 1500,
        "fuel_type": "Petrol", "condition": "Excellent",
        "city": "Seattle", "state": "WA",
    },
    {
        "title": "Triumph Street Triple RS",
        "brand": "Triumph", "model": "Street Triple RS", "year": 2020,
        "engine_cc": 765, "price": Decimal('8500.00'), "mileage": 11000,
        "fuel_type": "Petrol", "condition": "Good",
        "city": "Austin", "state": "TX",
    },
    {
        "title": "KTM 390 Duke - City Commuter",
        "brand": "KTM", "model": "390 Duke", "year": 2018,
        "engine_cc": 373, "price": Decimal('3800.00'), "mileage": 18000,
        "fuel_type": "Petrol", "condition": "Good",
        "city": "Denver", "state": "CO",
    },
    {
        "title": "Royal Enfield Continental GT 650",
        "brand": "Royal Enfield", "model": "Continental GT 650", "year": 2021,
        "engine_cc": 648, "price": Decimal('5800.00'), "mileage": 6000,
        "fuel_type": "Petrol", "condition": "Excellent",
        "city": "Portland", "state": "OR",
    },
    {
        "title": "Harley-Davidson Iron 883 Classic",
        "brand": "Harley-Davidson", "model": "Iron 883", "year": 2016,
        "engine_cc": 883, "price": Decimal('7500.00'), "mileage": 22000,
        "fuel_type": "Petrol", "condition": "Good",
        "city": "Nashville", "state": "TN",
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample bike listings'

    def handle(self, *args, **options):
        # Get or create a demo seller account
        seller, created = User.objects.get_or_create(
            email='demo_seller@bikemarketplace.com',
            defaults={
                'username': 'demo_seller',
                'first_name': 'Demo',
                'last_name': 'Seller',
            }
        )
        if created:
            seller.set_password('DemoSeller@123!')
            seller.save()
            self.stdout.write(self.style.SUCCESS('Created demo seller account.'))

        added = 0
        for data in BIKES_DATA:
            description = (
                f"This is a {data['condition'].lower()} condition "
                f"{data['year']} {data['brand']} {data['model']} "
                f"with {data['mileage']} miles. "
                f"Engine capacity: {data['engine_cc']}cc. "
                f"Contact the seller for more details!"
            )
            bike, created = Bike.objects.get_or_create(
                title=data['title'],
                defaults={
                    **data,
                    'seller': seller,
                    'description': description,
                    'status': 'Approved',
                    'ownership_number': random.randint(1, 2),
                    'negotiable': True,
                    'accident_history': False,
                }
            )
            if created:
                added += 1
                self.stdout.write(f'  + Added: {bike.title}')
            else:
                self.stdout.write(f'  ~ Skipped (already exists): {bike.title}')

        self.stdout.write(self.style.SUCCESS(f'Done! {added} new bike(s) added.'))
