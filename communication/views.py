from rest_framework import generics
from .models import SentimentAnalysis, BehavioralMetrics, Conversation, Message
from .insta_msg import group_messages_into_conversations
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    SentimentAnalysisSerializer,
    BehavioralMetricsSerializer,
    ConversationSerializer,
    MessageSerializer,
)

# Sentiment Analysis Views
class SentimentAnalysisListCreateView(generics.ListCreateAPIView):
    queryset = SentimentAnalysis.objects.all()
    serializer_class = SentimentAnalysisSerializer

class SentimentAnalysisDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SentimentAnalysis.objects.all()
    serializer_class = SentimentAnalysisSerializer

# Behavioral Metrics Views
class BehavioralMetricsListCreateView(generics.ListCreateAPIView):
    queryset = BehavioralMetrics.objects.all()
    serializer_class = BehavioralMetricsSerializer

class BehavioralMetricsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BehavioralMetrics.objects.all()
    serializer_class = BehavioralMetricsSerializer

# Conversation Views
class ConversationListCreateView(generics.ListCreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

# Message Views
class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class GroupMessagesView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            group_messages_into_conversations()  # Call the function to group messages
            return Response({"message": "Messages grouped into conversations successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)