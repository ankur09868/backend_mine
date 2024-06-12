from django.db import models
# from accounts.models import Account  # Import the Account model
from tenant.models import Tenant  # Import the Tenant model
from django.db import models
from django.conf import settings

class CustomField(models.Model):
    MODEL_CHOICES = (
        ('account', 'Account'),
        ('calls', 'Calls'),
        ('lead', 'Lead'),
        ('interaction','Interaction'),
    
    )

    FIELD_TYPE_CHOICES = (
        ('char', 'CharField'),
        ('text', 'TextField'),
        ('int', 'IntegerField'),
        ('float', 'FloatField'),
        ('bool', 'BooleanField'),
        ('date', 'DateField'),
        ('datetime', 'DateTimeField'),
        ('email', 'EmailField'),
        ('url', 'URLField'),
    )

    model_name = models.CharField(max_length=20, choices=MODEL_CHOICES)
    custom_field = models.CharField(max_length=255)
    value = models.TextField(blank=True, null=True)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES)
    user_id = models.IntegerField()  # Field to store the user ID
    tenant_id = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)