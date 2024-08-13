from rest_framework import serializers
from .models import Interaction,calls, meetings, Conversation

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = "__all__"

class callsSerializer(serializers.ModelSerializer):
    class Meta:
        model = calls
        fields = "__all__"


class meetingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = meetings
        fields = "__all__"

class WhatsappCSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = "__all__"