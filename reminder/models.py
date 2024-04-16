from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Reminder(models.Model):
    EVENT_TRIGGER = 'event'
    TIME_TRIGGER = 'time'
    TRIGGER_CHOICES = [
        (EVENT_TRIGGER, 'Event Trigger'),
        (TIME_TRIGGER, 'Time Trigger'),
    ]
    
    subject = models.CharField(max_length=255)
    trigger_type = models.CharField(max_length=10, choices=TRIGGER_CHOICES)
    event_date_time = models.DateTimeField(blank=True, null=True)
    time_trigger = models.DateTimeField(blank=True, null=True)
    is_triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    createdBy = models.ForeignKey(User, related_name='reminder_created_by', on_delete=models.CASCADE)

    def __str__(self):
        return self.subject
