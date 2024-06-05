from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class NodeTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='node_temp_createdby', on_delete=models.CASCADE,null=True)
    node_data = models.JSONField()

    def __str__(self):
        return self.name
