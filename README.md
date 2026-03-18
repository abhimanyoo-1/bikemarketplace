# SecondHand Bike Marketplace

A complete Django web application for buying and selling second-hand bikes.

## Features
- **Homepage:** Displays featured bikes.
- **Bike Listings:** Browse all available bikes with filters for brand, fuel type, and condition.
- **Bike Detail:** Detailed view of bikes with specifications and seller details.
- **Sell Bike Form:** List a new bike for sale (saves to `Bike` model and media folder).
- **Contact Seller Form:** Send an inquiry to a seller (saves to `Inquiry` model).
- **User Dashboard:** A simple listing page to see listed bikes.
- **Admin Panel:** Built-in Django admin integration to easily manage Bike properties and Inquiries.
- **UI:** A modern, custom-built UI that uses responsive grid/flexbox layouts and a clean aesthetic color palette.

## Project Structure
Standard Django project setup:
- `bike_marketplace/` - Core Django settings, URLs, ASGI/WSGI.
- `bikes/` - Main application with models (`Bike`, `Inquiry`), views, forms, and URLs.
- `templates/` - HTML templates overriding standard generic views.
- `static/css/` - Custom CSS styling (`style.css`).
- `media/bike_images/` - Upload directory for bike image listings.

## How to Run Locally

If you are just getting started, follow these instructions. Open a terminal or PowerShell in this directory.

```bash
# 1. Install required packages
pip install django pillow

# 2. Setup the database
python manage.py makemigrations
python manage.py migrate

# 3. Create a superuser for the admin panel
python manage.py createsuperuser

# 4. Starting the development server
python manage.py runserver
```

Once running, navigate to `http://127.0.0.1:8000/` to test the site. 
Navigate to `http://127.0.0.1:8000/admin/` to manage bikes and inquiries using your created superuser.
