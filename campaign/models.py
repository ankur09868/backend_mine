# campaign/models.py

from django.db import models
from django.conf import settings
from tenant.models import Tenant 
class Campaign(models.Model):
    campaign_owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='campaign_created_by', on_delete=models.CASCADE,blank=True, null=True)
    campaign_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    expected_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2)
    numbers_sent = models.IntegerField()
    type = models.CharField(max_length=50, choices=[('None', 'None'), ('Email', 'Email'), ('SMS', 'SMS')])
    status = models.CharField(max_length=50, choices=[('None', 'None'), ('Active', 'Active'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
    budgeted_cost = models.DecimalField(max_digits=10, decimal_places=2)
    expected_response = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE,default=3)

    def __str__(self):
        return self.campaign_name
