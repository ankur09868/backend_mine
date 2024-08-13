from rest_framework import serializers
from .models import SentimentAnalysis, BehavioralMetrics, Conversation, Message

class SentimentAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentAnalysis
        fields = '__all__'  # Include all fields

class BehavioralMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehavioralMetrics
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
