from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bikes/', views.bike_list, name='bike_list'),
    path('bikes/<int:pk>/', views.bike_detail, name='bike_detail'),
    path('sell/', views.sell_bike, name='sell_bike'),
    path('contact/<int:pk>/', views.contact_seller, name='contact_seller'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('favorites/toggle/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('listings/delete/<int:pk>/', views.delete_listing, name='delete_listing'),
]
