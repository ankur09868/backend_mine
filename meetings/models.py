from django.contrib.auth.models import User
from contacts.models import Contact
from django.conf import settings
from django.db import models
from tenant.models import Tenant 
class meetings(models.Model):
    title = models.CharField(max_length=64, blank=True, null=True, verbose_name='Title')
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name='Location')
    from_time = models.DateTimeField(verbose_name='From')
    to_time = models.DateTimeField(verbose_name='To')
    related_to = models.CharField(max_length=255, blank=True, null=True, verbose_name='Related To')
    contact_name = models.ForeignKey(Contact, on_delete=models.SET_NULL, related_name='meeting_contacts', blank=True, null=True, verbose_name='Contact Name')
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='meeting_hosts', blank=True, null=True, verbose_name='Host')
    participants = models.ManyToManyField(Contact, related_name='meeting_participants', blank=True)
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    account = models.ForeignKey('accounts.Account', related_name='meetings', on_delete=models.CASCADE, blank=True, null=True)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='meeting_assigned_users',blank=True, null=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='meeting_created_by', on_delete=models.CASCADE,blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
