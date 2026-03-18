from django.contrib import admin
from .models import Bike, BikeImage, Inquiry, Favorite


class BikeImageInline(admin.TabularInline):
    model = BikeImage
    extra = 1


def approve_listings(modeladmin, request, queryset):
    queryset.update(status='Approved')
approve_listings.short_description = "✓ Approve selected listings"


def reject_listings(modeladmin, request, queryset):
    queryset.update(status='Rejected')
reject_listings.short_description = "✗ Reject selected listings"


def mark_sold(modeladmin, request, queryset):
    queryset.update(status='Sold')
mark_sold.short_description = "Mark selected listings as Sold"


@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'model', 'year', 'price', 'status', 'seller', 'created_at')
    search_fields = ('title', 'brand', 'model', 'city', 'state', 'seller__email')
    list_filter = ('status', 'brand', 'year', 'fuel_type', 'condition')
    list_editable = ('status',)
    actions = [approve_listings, reject_listings, mark_sold]
    inlines = [BikeImageInline]
    readonly_fields = ('created_at',)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('buyer_name', 'bike', 'email', 'inquiry_date')
    search_fields = ('buyer_name', 'email', 'bike__title')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'bike', 'created_at')
    search_fields = ('user__email', 'bike__title')
