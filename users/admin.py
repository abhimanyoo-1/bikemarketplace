from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'phone_number', 'is_verified', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Seller Info', {'fields': ('phone_number', 'location', 'profile_photo', 'seller_rating', 'is_verified')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
