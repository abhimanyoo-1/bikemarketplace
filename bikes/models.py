from django.db import models
from django.utils import timezone
from django.conf import settings

class Bike(models.Model):
    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Electric', 'Electric'),
        ('Diesel', 'Diesel'),
    ]
    CONDITION_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Sold', 'Sold'),
        ('Expired', 'Expired'),
    ]

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bikes')
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    engine_cc = models.IntegerField(help_text="Engine capacity in CC", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.IntegerField(help_text="Mileage in km or miles")
    ownership_number = models.IntegerField(default=1, help_text="Number of previous owners")
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    
    city = models.CharField(max_length=100, default='Unknown')
    state = models.CharField(max_length=100, default='Unknown')
    
    registration_state = models.CharField(max_length=100, blank=True, null=True)
    insurance_validity = models.DateField(blank=True, null=True)
    service_history = models.BooleanField(default=False, help_text="Full service history available?")
    negotiable = models.BooleanField(default=True)
    
    accident_history = models.BooleanField(default=False)
    modifications = models.TextField(blank=True, null=True)
    warranty_remaining = models.BooleanField(default=False)
    
    description = models.TextField()
    video = models.FileField(upload_to='bike_videos/', null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

class BikeImage(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='bike_images/')
    
    def __str__(self):
        return f"Image for {self.bike.title}"

class Inquiry(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='inquiries')
    buyer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    inquiry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry for {self.bike.title} by {self.buyer_name}"

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'bike')

    def __str__(self):
        return f"{self.user.email} → {self.bike.title}"
