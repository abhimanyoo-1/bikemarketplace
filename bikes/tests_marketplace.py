from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser
from bikes.models import Bike, Favorite

class MarketplaceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='password123'
        )
        self.bike = Bike.objects.create(
            title='Test Bike',
            brand='Yamaha',
            model='R1',
            year=2024,
            price=2000000,
            mileage=1000,
            fuel_type='Petrol',
            condition='Excellent',
            city='Mumbai',
            state='Maharashtra',
            seller=self.user,
            status='Approved'
        )
        # Use force_login instead of self.client.login to avoid allauth session issues in tests
        self.client.force_login(self.user)

    def test_toggle_favorite(self):
        # 1. Add to favorites
        url = reverse('toggle_favorite', kwargs={'pk': self.bike.pk})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Favorite.objects.filter(user=self.user, bike=self.bike).exists())

        # 2. Remove from favorites
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Favorite.objects.filter(user=self.user, bike=self.bike).exists())

    def test_favorites_list_view(self):
        Favorite.objects.create(user=self.user, bike=self.bike)
        url = reverse('favorites_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yamaha R1')

    def test_dashboard_stats(self):
        Favorite.objects.create(user=self.user, bike=self.bike)
        url = reverse('user_dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Check if favorite count and listing count are present in context
        self.assertEqual(response.context['favorites_count'], 1)
        self.assertEqual(len(response.context['bikes']), 1)

    def test_delete_listing(self):
        url = reverse('delete_listing', kwargs={'pk': self.bike.pk})
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Bike.objects.filter(pk=self.bike.pk).exists())
