# campaign/serializers.py

from rest_framework import serializers
from .models import Campaign
from .models import InstagramCampaign
from .models import EmailCampaign

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'


class InstagramCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramCampaign
        fields = '__all__'  # Or specify the fields you want to include

    def validate(self, attrs):
        # Add any custom validation logic here
        return attrs
from .models import WhatsAppCampaign

class WhatsAppCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppCampaign
        fields = '__all__'  # Or specify the fields you want to include

    def validate(self, attrs):
        # Add any custom validation logic here
        return attrs

class EmailCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailCampaign
        fields = '__all__'  # Or specify the fields you want to include

    def validate(self, attrs):
        # Add any custom validation logic here
        if 'recipient_list' in attrs:
            # Example validation: Ensure recipient list is not empty
            if not attrs['recipient_list']:
                raise serializers.ValidationError("Recipient list cannot be empty.")
        return attrs

