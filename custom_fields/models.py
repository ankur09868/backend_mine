from django.db import models
# from accounts.models import Account  # Import the Account model
from tenant.models import Tenant  # Import the Tenant model
from django.db import models
from django.conf import settings
from django.db.models import Max


class CustomField(models.Model):
    MODEL_CHOICES = (
        ('account', 'Account'),
        ('calls', 'calls'),
        ('lead', 'Lead'),
        ('interaction','Interaction'),
        ('conatact','Contact'),
    
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
    user_id = models.IntegerField(default=7) 
    tenant_id = models.IntegerField(default=3)
    entity_id = models.IntegerField(default=1, editable=False)  # set editable to False

    def save(self, *args, **kwargs):
        if self.model_name and self.custom_field:
            self.custom_field = f"{self.model_name}_{self.custom_field}"
        
            if not self.pk:  # Only set entity_id for new objects
                max_entity_id = CustomField.objects.filter(
                    model_name=self.model_name,
                    custom_field=self.custom_field
                ).aggregate(Max('entity_id'))['entity_id__max']

                if max_entity_id is not None:
                    self.entity_id = max_entity_id + 1
                else:
                    self.entity_id = 1
        
        super().save(*args, **kwargs)