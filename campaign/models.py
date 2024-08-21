# campaign/models.py

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from tenant.models import Tenant 
class Campaign(models.Model):
    campaign_owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='campaign_created_by', on_delete=models.CASCADE,blank=True, null=True)
    campaign_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    expected_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2)
    numbers_sent = models.IntegerField()
      # Change type field to an ArrayField
    type = ArrayField(
        models.CharField(max_length=50, choices=[('Email', 'Email'),('CALL', 'CALL'),('WHATSAPP', 'WHATSAPP'),('INSTAGRAM', 'INSTAGRAM')]), 
        blank=True,
        default=list
    )
    status = models.CharField(max_length=50, choices=[('None', 'None'), ('Active', 'Active'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
    budgeted_cost = models.DecimalField(max_digits=10, decimal_places=2)
    expected_response = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE,default=3)

    def __str__(self):
        return self.campaign_name
    

class InstagramCampaign(models.Model):
    # Foreign key to the Campaign model
    campaign = models.OneToOneField(Campaign, related_name='instagram_campaign', on_delete=models.CASCADE)

    # General fields for Instagram campaigns
    campaign_tone = models.CharField(max_length=50, choices=[
        ('Informative', 'Informative'),
        ('Promotional', 'Promotional'),
        ('Engaging', 'Engaging'),
        ('Storytelling', 'Storytelling'),
    ], default='Promotional')  # Tone of the campaign

    number_of_posts = models.IntegerField(default=1)  # Total number of posts planned for the campaign
    target_hashtags = models.TextField(blank=True, null=True)  # Target hashtags for the campaign
    duration = models.DurationField(blank=True, null=True)  # Duration of the campaign
    audience_targeting = models.CharField(max_length=255, blank=True, null=True)  # Description of the target audience
    call_to_action = models.CharField(max_length=255, blank=True, null=True)  # General call to action for the campaign

    # Metrics for tracking performance
    engagement_goal = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Expected engagement rate
    actual_engagement = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Actual engagement rate
    notes = models.TextField(blank=True, null=True)  # Additional notes about the campaign

    def __str__(self):
        return f"{self.campaign.campaign_name} - Instagram Campaign"

    class Meta:
        verbose_name = "Instagram Campaign"
        verbose_name_plural = "Instagram Campaigns"

class WhatsAppCampaign(models.Model):
    # Foreign key to the Campaign model
    campaign = models.OneToOneField(Campaign, related_name='whatsapp_campaign', on_delete=models.CASCADE)

    # Specific fields for WhatsApp campaigns
    broadcast_message = models.TextField(blank=True, null=True)  # Message to broadcast
    chatbot_enabled = models.BooleanField(default=False)  # Whether a chatbot is enabled for this campaign
    chatbot_script = models.TextField(blank=True, null=True)  # Script for the chatbot interactions
    ai_integration = models.BooleanField(default=False)  # Whether AI features are integrated
    ai_features = models.TextField(blank=True, null=True)  # Details about AI features used
    target_audience = models.CharField(max_length=255, blank=True, null=True)  # Description of the target audience
    message_template = models.TextField(blank=True, null=True)  # Template for messages to be sent
    number_of_recipients = models.IntegerField(default=0)  # Number of recipients for the campaign
    scheduling_time = models.DateTimeField(blank=True, null=True)  # When the messages should be sent

    # Metrics for tracking performance
    engagement_goal = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Expected engagement rate
    actual_engagement = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Actual engagement rate
    notes = models.TextField(blank=True, null=True)  # Additional notes about the campaign

    def __str__(self):
        return f"{self.campaign.campaign_name} - WhatsApp Campaign"

    class Meta:
        verbose_name = "WhatsApp Campaign"
        verbose_name_plural = "WhatsApp Campaigns"

class EmailCampaign(models.Model):
    # Foreign key to the Campaign model
    campaign = models.OneToOneField(Campaign, related_name='email_campaign', on_delete=models.CASCADE)

    # Specific fields for email campaigns
    subject_line = models.CharField(max_length=255)  # Subject line of the email
    email_body = models.TextField()  # Body of the email
    sender_email = models.EmailField()  # Sender's email address
    recipient_list = models.TextField(blank=True, null=True)  # Comma-separated list of recipient emails
    scheduled_time = models.DateTimeField(blank=True, null=True)  # When the email should be sent
    email_template = models.TextField(blank=True, null=True)  # Template used for the email

    # Tracking metrics
    emails_sent = models.IntegerField(default=0)  # Number of emails sent
    emails_opened = models.IntegerField(default=0)  # Number of emails opened
    clicks = models.IntegerField(default=0)  # Number of links clicked in the email
    bounces = models.IntegerField(default=0)  # Number of bounced emails
    unsubscribes = models.IntegerField(default=0)  # Number of unsubscribes from the email list
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Engagement rate of the campaign
    notes = models.TextField(blank=True, null=True)  # Additional notes about the campaign
    email_html = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.campaign.campaign_name} - Email Campaign"

    class Meta:
        verbose_name = "Email Campaign"
        verbose_name_plural = "Email Campaigns"