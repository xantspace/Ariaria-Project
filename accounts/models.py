from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    phone_number = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    business_name = models.CharField(max_length=50)

    def __str__(self):
        return self.username
    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = {
        'pending': 'Pending',
        'shipped' : 'Shipped',
        'delivered' : 'Delivered',
        'cancelled' : 'Cancelled',
    }
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
