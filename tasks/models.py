from django.db import models
from django.contrib.auth.models import User
from contacts.models import Contact
from accounts.models import Account
from django.conf import settings
from tenant.models import Tenant 
class Tasks(models.Model):
    STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('deferred', 'Deferred'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('waiting_for_input', 'Waiting for Input'),
    )

    PRIORITY_CHOICES = (
        ('high', 'High'),
        ('normal', 'Normal'),
        ('low', 'Low'),
    )

    subject = models.CharField(max_length=255)
    due_date = models.DateField()
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='task_created_by', on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, related_name='contact_tasks', on_delete=models.CASCADE, blank=True, null=True)
    account = models.ForeignKey(Account, related_name='account_tasks', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    reminder = models.BooleanField(default=False)
    description = models.TextField()
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.subject
