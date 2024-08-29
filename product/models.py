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
    experience_name = models.CharField(max_length=200, null=True)
    highlights = models.TextField(null=True)
    slot_timing = models.CharField(max_length=200, null=True)
    sale_price = models.CharField(max_length=255, null=True)
    tax = models.CharField(max_length=255, null=True)
    duration_in_hours = models.CharField(max_length=100 , null=True, blank=True)
    itenerary = models.TextField(null=True)
    itenerary_time = models.TextField(null=True)
    inclusions_and_exclusions = models.TextField(null=True)
    additional_information = models.TextField(null=True)
    time_of_the_day = models.CharField(max_length=50, null=True)
    vendor_owner = models.CharField(max_length=255, null=True)
    experience = models.TextField(null=True)
    eligibility = models.CharField(max_length=200, null=True)
    proibitions_and_limitations = models.TextField(null=True)
    what_to_bring = models.TextField(null=True)
    terms_and_cancellations = models.TextField(null=True)
    insider_tip = models.TextField(null=True)
    description = models.TextField(null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.experience_name
