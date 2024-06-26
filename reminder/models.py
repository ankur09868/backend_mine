from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from tenant.models import Tenant 
class Reminder(models.Model):
    EVENT_TRIGGER = 'event'
    TIME_TRIGGER = 'time'
    TRIGGER_CHOICES = [
        (EVENT_TRIGGER, 'Event Trigger'),
        (TIME_TRIGGER, 'Time Trigger'),
    ]
    
    subject = models.CharField(max_length=255)
    
    event_date_time = models.DateTimeField(blank=True, null=True)
    time_trigger = models.DateTimeField(blank=True, null=True)
    is_triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reminder_created_by', on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    def __str__(self):
        return self.subject
