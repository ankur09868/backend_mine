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
 