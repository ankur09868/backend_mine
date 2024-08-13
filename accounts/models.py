from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from tenant.models import Tenant


INDCHOICES = (
    ('FINANCE', 'FINANCE'),
    ('HEALTHCARE', 'HEALTHCARE'),
    ('INSURANCE', 'INSURANCE'),
    ('LEGAL', 'LEGAL'),
    ('MANUFACTURING', 'MANUFACTURING'),
    ('PUBLISHING', 'PUBLISHING'),
    ('REAL ESTATE', 'REAL ESTATE'),
    ('SOFTWARE', 'SOFTWARE'),
)

ACCOUNT_TYPE_CHOICES = [
    ('business', 'Business'),
    ('consumer', 'Consumer'),
]

# Define the choices for account stages
STAGE_CHOICES = [
    ("Prospect", "Prospect"),
    ("Engaged Prospect", "Engaged Prospect"),
    ("Lead", "Lead"),
    ("Shopping Cart", "Shopping Cart"),
    ("Checkout", "Checkout"),
    ("New Customer", "New Customer"),
    ("Product Setup", "Product Setup"),
    ("First Use", "First Use"),
    ("Active Customer", "Active Customer"),
    ("Support", "Support"),
    ("Feedback", "Feedback"),
    ("Loyalty Programs", "Loyalty Programs"),
    ("Re-Engagement", "Re-Engagement"),
    ("Upsell", "Upsell"),
    ("Cross-Sell", "Cross-Sell"),
    ("Referrals", "Referrals"),
    ("At-Risk Customer", "At-Risk Customer"),
    ("Lost Customer", "Lost Customer"),
]

class Account(models.Model):
    Name = models.CharField("Name of Account", max_length=64)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    industry = models.CharField("Industry Type", max_length=255, blank=True, null=True)
    website = models.URLField("Website", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='account_assigned_to', blank=True, null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='account_created_by', on_delete=models.CASCADE, blank=True, null=True)
    createdOn = models.DateTimeField("Created on", auto_now_add=True)
    is_active = models.BooleanField(default=False)
    company = models.CharField(max_length=100, default='Unknown')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE )
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, null=True)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, blank=True, null=True)
   # custom_fields = models.ForeignKey(CustomField, on_delete=models.CASCADE, null=True, blank=True, related_name='account_custom_fields')




    def __str__(self):
        return self.name
    
    

  