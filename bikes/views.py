from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Bike, BikeImage, Inquiry, Favorite
from .forms import BikeForm, InquiryForm


def home(request):
    featured_bikes = Bike.objects.filter(status='Approved').order_by('-created_at')[:6]
    total_bikes = Bike.objects.filter(status='Approved').count()
    stats = [
        ('Bikes Listed', total_bikes),
        ('Happy Sellers', 'Growing'),
        ('Cities Covered', 'Pan-India'),
    ]
    return render(request, 'home.html', {'featured_bikes': featured_bikes, 'stats': stats})


def bike_list(request):
    bikes = Bike.objects.filter(status='Approved').order_by('-created_at')

    # Global Search
    q = request.GET.get('q')
    if q:
        bikes = bikes.filter(
            Q(brand__icontains=q) |
            Q(model__icontains=q) |
            Q(city__icontains=q) |
            Q(state__icontains=q) |
            Q(description__icontains=q)
        )

    brand = request.GET.get('brand')
    if brand:
        bikes = bikes.filter(brand__icontains=brand)

    fuel_type = request.GET.get('fuel_type')
    if fuel_type:
        bikes = bikes.filter(fuel_type=fuel_type)

    condition = request.GET.get('condition')
    if condition:
        bikes = bikes.filter(condition=condition)

    min_price = request.GET.get('min_price')
    if min_price:
        bikes = bikes.filter(price__gte=min_price)

    max_price = request.GET.get('max_price')
    if max_price:
        bikes = bikes.filter(price__lte=max_price)

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        bikes = bikes.order_by('price')
    elif sort == 'price_desc':
        bikes = bikes.order_by('-price')
    elif sort == 'mileage_asc':
        bikes = bikes.order_by('mileage')

    return render(request, 'bike_list.html', {'bikes': bikes})


def bike_detail(request, pk):
    bike = get_object_or_404(Bike, pk=pk)
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, bike=bike).exists()
    return render(request, 'bike_detail.html', {'bike': bike, 'is_favorited': is_favorited})


@login_required
def sell_bike(request):
    if request.method == 'POST':
        form = BikeForm(request.POST, request.FILES)
        if form.is_valid():
            bike = form.save(commit=False)
            bike.seller = request.user
            bike.save()

            # Handle multiple images (up to 10)
            images = request.FILES.getlist('images')
            for index, image in enumerate(images):
                if index < 10:
                    BikeImage.objects.create(bike=bike, image=image)

            messages.success(request, 'Your bike has been listed! It is pending approval.')
            return redirect('bike_detail', pk=bike.pk)
    else:
        form = BikeForm()
    return render(request, 'sell_bike.html', {'form': form})


def contact_seller(request, pk):
    bike = get_object_or_404(Bike, pk=pk)
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.bike = bike
            inquiry.save()
            messages.success(request, 'Your inquiry has been sent to the seller!')
            return redirect('bike_detail', pk=bike.pk)
    else:
        form = InquiryForm()
    return render(request, 'contact_seller.html', {'form': form, 'bike': bike})


@login_required
def user_dashboard(request):
    bikes = Bike.objects.filter(seller=request.user).order_by('-created_at')
    favorites_count = Favorite.objects.filter(user=request.user).count()
    return render(request, 'user_dashboard.html', {'bikes': bikes, 'favorites_count': favorites_count})


@login_required
def toggle_favorite(request, pk):
    bike = get_object_or_404(Bike, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, bike=bike)
    if not created:
        fav.delete()
        messages.success(request, f'Removed "{bike.brand} {bike.model}" from your favorites.')
    else:
        messages.success(request, f'Added "{bike.brand} {bike.model}" to your favorites!')
    return redirect('bike_detail', pk=pk)


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('bike').order_by('-created_at')
    return render(request, 'favorites.html', {'favorites': favorites})


@login_required
def delete_listing(request, pk):
    bike = get_object_or_404(Bike, pk=pk, seller=request.user)
    if request.method == 'POST':
        bike.delete()
        messages.success(request, 'Listing deleted successfully.')
    return redirect('user_dashboard')
