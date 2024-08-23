from rest_framework import serializers
from .models import Interaction, Calls, Meetings, Conversation
from .models import Interaction,calls, meetings, Conversation,Email

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = "__all__"

class callsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calls
        fields = "__all__"


class meetingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meetings
        fields = "__all__"

class WhatsappCSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = "__all__"

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = "__all__"