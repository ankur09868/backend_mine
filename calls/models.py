from django.db import models
from django.conf import settings
from contacts.models import Contact
from tenant.models import Tenant 
from campaign.models import Campaign
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
    
class CallCampaign(models.Model):
    # Foreign key to the Campaign model
    campaign = models.ForeignKey(Campaign, related_name='call_campaigns', on_delete=models.CASCADE)
    
    # New fields for call campaigns
    campaign_type = models.CharField(max_length=50, choices=[
        ('Outbound', 'Outbound'),
        ('Inbound', 'Inbound'),
        ('Follow-Up', 'Follow-Up'),
        ('Survey', 'Survey'),
        ('Sales', 'Sales'),
    ], default='Outbound')  # Type of call campaign
    
    call_script = models.TextField(blank=True, null=True)  # The script for the calls
    contacts = models.ManyToManyField(Contact, related_name='call_campaigns', blank=True)  # List of contacts to call
    
    scheduled_time = models.DateTimeField(blank=True, null=True)  # When the calls should be made
    duration = models.DurationField(blank=True, null=True)  # Expected duration of the calls
    
    # Keeping status simple, could also use a more generic approach
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ], default='Pending')  # Status of the call campaign
    
    # Expected and actual response rates can be derived from the Campaign if needed
    notes = models.TextField(blank=True, null=True)  # Additional notes about the campaign

    def __str__(self):
        return f"{self.campaign.campaign_name} - {self.campaign_type}"

    class Meta:
        unique_together = ('campaign', 'campaign_type')  # Ensure uniqueness for campaign types within the same campaign
    # Foreign key to the Campaign model
    campaign = models.ForeignKey(Campaign, related_name='call_campaigns', on_delete=models.CASCADE)
    
    # New fields for call campaigns
    campaign_type = models.CharField(max_length=50, choices=[
        ('Outbound', 'Outbound'),
        ('Inbound', 'Inbound'),
        ('Follow-Up', 'Follow-Up'),
        ('Survey', 'Survey'),
        ('Sales', 'Sales'),
    ], default='Outbound')  # Type of call campaign
    
    call_script = models.TextField(blank=True, null=True)  # The script for the calls
    contacts = models.ManyToManyField(Contact, related_name='call_campaigns', blank=True)  # List of contacts to call
    
    scheduled_time = models.DateTimeField(blank=True, null=True)  # When the calls should be made
    duration = models.DurationField(blank=True, null=True)  # Expected duration of the calls
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ], default='Pending')  # Status of the call campaign
    
    expected_response_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Expected response rate
    actual_response_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Actual response rate
    notes = models.TextField(blank=True, null=True)  # Additional notes about the campaign


    def __str__(self):
        return f"{self.campaign.campaign_name} - {self.campaign_type}"
    
