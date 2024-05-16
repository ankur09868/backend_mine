from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from tenant.models import Tenant 
class Interaction(models.Model):
    INTERACTION_TYPES = (
        ('Call', 'Call'),
        ('Email', 'Email'),
        ('Meeting', 'Meeting'),
        ('Note', 'Note'),
       
    )

    entity_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    entity_id = models.PositiveIntegerField()
    entity = GenericForeignKey('entity_type', 'entity_id')
    
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_TYPES)
    interaction_datetime = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.interaction_type} with {self.entity}'
