from rest_framework import serializers
from .models import calls
from .models import CallCampaign


class callsSerializer(serializers.ModelSerializer):
    class Meta:
        model = calls
        fields = "__all__"

class CallCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallCampaign
        fields = '__all__'  # Or specify the fields you want to include

    