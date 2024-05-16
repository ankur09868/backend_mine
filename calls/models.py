from django.db import models
from django.conf import settings
from contacts.models import Contact
from tenant.models import Tenant 
class calls(models.Model):
    call_to = models.ForeignKey(Contact, on_delete=models.SET_NULL, related_name='call_to_meetings', blank=True, null=True, verbose_name='Contact Name')
    related_to = models.CharField(max_length=255, blank=True, null=True, verbose_name='Related To')
    call_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='Call Type')
    outgoing_status = models.CharField(max_length=255, blank=True, null=True, verbose_name='Outgoing Status')
    start_time = models.DateTimeField(verbose_name='Start Time', blank=True, null=True)
    call_duration = models.DurationField(verbose_name='Call Duration', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name='Location')
    voice_recording = models.CharField(max_length=255, blank=True, null=True, verbose_name='Voice Recording')
    to_time = models.DateTimeField(verbose_name='To', blank=True, null=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_calls', on_delete=models.CASCADE, blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
