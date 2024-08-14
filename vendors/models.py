from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from tenant.models import Tenant 

class Vendors(models.Model):
    vendor_owner = models.CharField(max_length=100)
    vendor_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    website = models.URLField(max_length=200, blank=True)
    category = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    


    def __str__(self):
        return self.vendor_name

