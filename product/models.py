from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from tenant.models import Tenant 
from vendors.models import Vendors

class Product(models.Model):
    product_owner = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=50, unique=True)
    vendor_name = models.CharField(max_length=100, null=True)
    product_active = models.BooleanField(default=True)
    manufacturer = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100)
    sales_start_date = models.DateField(null=True, blank=True)
    sales_end_date = models.DateField(null=True, blank=True)
    support_start_date = models.DateField(null=True, blank=True)
    support_end_date = models.DateField(null=True, blank=True)
    unit_price = models.CharField(max_length=200, null=True, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    is_taxable = models.BooleanField(default=False)
    usage_unit = models.CharField(max_length=50)
    qty_ordered = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    handler = models.CharField(max_length=100)
    quantity_in_demand = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
  


    def __str__(self):
        return f'{self.product_name} ({self.product_code})'
 
class Experience(models.Model):
    experience_name = models.CharField(max_length=200)
    highlights = models.TextField()
    slot_timing = models.CharField(max_length=100)
    sale_price = models.IntegerField()
    tax = models.IntegerField()
    duration_in_hours = models.IntegerField()
    itenerary_description = models.TextField()
    itenerary_heading = models.CharField(max_length=100)
    itenerary_time = models.CharField(max_length=50)
    inclusions = models.CharField(max_length=100)
    exclusions = models.CharField(max_length=100)
    additional_information = models.CharField(max_length=255)
    time_of_the_day = models.CharField(max_length=50)
    vendor_name = models.ForeignKey(Vendors, on_delete=models.CASCADE)