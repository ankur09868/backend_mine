from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from tenant.models import Tenant
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey 

class Document(models.Model):
    # Information about the document
    name = models.CharField('Document Name',max_length=600)
    document_type = models.CharField('Document Type',max_length=600)
    description = models.TextField('Description', blank=True)
    file_url = models.CharField('File URL', default='', max_length=600)
    # GenericForeignKey to associate with any entity
    entity_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    entity_id = models.PositiveIntegerField(blank=True, null=True)
    entity = GenericForeignKey('entity_type', 'entity_id')

    
    # Other metadata
    uploaded_at = models.DateTimeField('Uploaded At', auto_now_add=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return self.name