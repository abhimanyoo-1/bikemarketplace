import os
import django
import random
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bike_marketplace.settings')
django.setup()

from django.contrib.auth import get_user_model
from bikes.models import Bike, BikeImage

User = get_user_model()

# Create dummy users if they don't exist
user1, _ = User.objects.get_or_create(email="seller1@example.com", defaults={"first_name": "John", "last_name": "Doe", "username": "seller1"})
if _:
    user1.set_password("password123")
    user1.save()

user2, _ = User.objects.get_or_create(email="seller2@example.com", defaults={"first_name": "Jane", "last_name": "Smith", "username": "seller2"})
if _:
    user2.set_password("password123")
    user2.save()

BRANDS = ['Yamaha', 'Honda', 'Suzuki', 'Kawasaki', 'Ducati', 'BMW', 'Triumph', 'KTM', 'Royal Enfield', 'Harley-Davidson']

# Sample data for bikes
bikes_data = [
    {
        "title": "Yamaha R1 in excellent condition",
        "brand": "Yamaha",
        "model": "YZF-R1",
        "year": 2021,
        "engine_cc": 998,
        "price": Decimal('14500.00'),
        "mileage": 8500,
        "fuel_type": "Petrol",
        "condition": "Excellent",
        "status": "Approved"
    },
    {
        "title": "Honda CBR600RR - Track Ready",
        "brand": "Honda",
        "model": "CBR600RR",
        "year": 2019,
        "engine_cc": 599,
        "price": Decimal('9500.00'),
        "mileage": 12000,
        "fuel_type": "Petrol",
        "condition": "Good",
        "status": "Approved"
    },
    {
        "title": "Suzuki GSX-R1000 - Low Mileage",
        "brand": "Suzuki",
        "model": "GSX-R1000",
        "year": 2020,
        "engine_cc": 999,
        "price": Decimal('12500.00'),
        "mileage": 5000,
        "fuel_type": "Petrol",
        "condition": "Excellent",
        "status": "Approved"
    },
    {
        "title": "Kawasaki Ninja 400 - Beginner Friendly",
        "brand": "Kawasaki",
        "model": "Ninja 400",
        "year": 2022,
        "engine_cc": 399,
        "price": Decimal('5200.00'),
        "mileage": 3000,
        "fuel_type": "Petrol",
        "condition": "Excellent",
        "status": "Approved"
    },
    {
        "title": "Ducati Panigale V2 - Needs TLC",
        "brand": "Ducati",
        "model": "Panigale V2",
        "year": 2021,
        "engine_cc": 955,
        "price": Decimal('13000.00'),
        "mileage": 15000,
        "fuel_type": "Petrol",
        "condition": "Fair",
        "status": "Approved"
    },
    {
        "title": "BMW S1000RR M Package",
        "brand": "BMW",
        "model": "S1000RR",
        "year": 2023,
        "engine_cc": 999,
        "price": Decimal('22500.00'),
        "mileage": 1500,
        "fuel_type": "Petrol",
        "condition": "Excellent",
        "status": "Approved"
    },
    {
        "title": "Triumph Street Triple RS",
        "brand": "Triumph",
        "model": "Street Triple RS",
        "year": 2020,
        "engine_cc": 765,
        "price": Decimal('8500.00'),
        "mileage": 11000,
        "fuel_type": "Petrol",
        "condition": "Good",
        "status": "Approved"
    },
    {
        "title": "KTM 390 Duke - City Commuter",
        "brand": "KTM",
        "model": "390 Duke",
        "year": 2018,
        "engine_cc": 373,
        "price": Decimal('3800.00'),
        "mileage": 18000,
        "fuel_type": "Petrol",
        "condition": "Good",
        "status": "Approved"
    },
    {
        "title": "Royal Enfield Continental GT 650",
        "brand": "Royal Enfield",
        "model": "Continental GT 650",
        "year": 2021,
        "engine_cc": 648,
        "price": Decimal('5800.00'),
        "mileage": 6000,
        "fuel_type": "Petrol",
        "condition": "Excellent",
        "status": "Approved"
    },
    {
        "title": "Harley-Davidson Iron 883 Classic",
        "brand": "Harley-Davidson",
        "model": "Iron 883",
        "year": 2016,
        "engine_cc": 883,
        "price": Decimal('7500.00'),
        "mileage": 22000,
        "fuel_type": "Petrol",
        "condition": "Good",
        "status": "Approved"
    }
]

# Create bikes
users = [user1, user2]
created_count = 0

print("Adding dummy bikes to database...")
for data in bikes_data:
    # Assign a random user as the seller
    seller = random.choice(users)
    
    # Defaults for required fields not in bikes_data
    defaults = {
        'city': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami']),
        'state': random.choice(['NY', 'CA', 'IL', 'TX', 'FL']),
        'description': f"This is a great {data['year']} {data['brand']} {data['model']}. It has {data['mileage']} miles and is in {data['condition']} condition. Contact me for more details!",
        'ownership_number': random.randint(1, 3),
        'negotiable': random.choice([True, False]),
        'accident_history': False,
    }
    
    # Merge exact data with defaults
    bike_attrs = {**data, **defaults}
    
    # Create or update based on title to avoid duplicates if run multiple times
    bike, created = Bike.objects.get_or_create(
        title=data['title'],
        seller=seller,
        defaults=bike_attrs
    )
    
    if not created:
        for attr, value in bike_attrs.items():
            setattr(bike, attr, value)
        bike.save()
        print(f"Updated: {bike.title}")
    else:
        created_count += 1
        print(f"Created: {bike.title}")

print(f"Finished! Successfully added/updated {len(bikes_data)} bikes.")
