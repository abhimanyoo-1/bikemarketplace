from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser

class ProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='password123'
        )
        self.client.force_login(self.user)

    def test_profile_update_persistence(self):
        url = reverse('profile_edit')
        data = {
            'first_name': 'Super',
            'last_name': 'Admin',
            'phone_number': '1234567890',
            'location': 'Pune, Maharashtra',
        }
        # POST to the profile edit view
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        
        # Refresh user from DB
        self.user.refresh_from_db()
        
        # Verify all fields updated correctly
        self.assertEqual(self.user.first_name, 'Super')
        self.assertEqual(self.user.last_name, 'Admin')
        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertEqual(self.user.location, 'Pune, Maharashtra')
        
    def test_search_functionality(self):
        from bikes.models import Bike
        Bike.objects.create(
            title='Unique Bike', brand='UniqueBrand', model='X1', year=2024,
            price=1000, mileage=10, fuel_type='Electric', condition='New',
            city='TestCity', state='TS', seller=self.user, status='Approved'
        )
        url = reverse('bike_list')
        
        # Test searching for brand
        response = self.client.get(url + '?q=UniqueBrand')
        self.assertContains(response, 'UniqueBrand')
        
        # Test searching for city
        response = self.client.get(url + '?q=TestCity')
        self.assertContains(response, 'UniqueBrand')
        
        # Test negative search
        response = self.client.get(url + '?q=NonExistent')
        self.assertNotContains(response, 'UniqueBrand')
